/*!
 * @file  receiveCheck.ino
 * @brief  CAN-BUS Shield, receive data with check mode
 * @n  send data coming to fast, such as less than 10ms, you can use this way
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license  The MIT License (MIT)
 * @author  Arduinolibrary
 * @maintainer  [qsjhyy](yihuan.huang@dfrobot.com)
 * @version  V1.0
 * @date  2022-05-25
 * @url  https://github.com/DFRobot/DFRobot_MCP2515
 */
#include "DFRobot_MCP2515.h"

const int SPI_CS_PIN = 10;
DFRobot_MCP2515 CAN(SPI_CS_PIN);   // Set CS pin

class PerformanceMonitor{
public:
PerformanceMonitor(const uint32_t print_interval, unsigned int timestamp_buffer_size):
    INTERVAL{print_interval},
    m_last_check{0},
    m_receive_count{0},
    m_timestamp_buffer_size{timestamp_buffer_size},
    m_timestamp_buffer_next_index{0}
{
    m_receive_timestamp_buffer = new unsigned long[m_timestamp_buffer_size];
}

~PerformanceMonitor()
{
    delete [] m_receive_timestamp_buffer;
}

void AddCount(unsigned long count)
{
  m_receive_count += count;
}

void RecordReceiveTime(const unsigned long current_time)
{
    // Overflown.
    if (m_timestamp_buffer_next_index == m_timestamp_buffer_size)
    {
        return;
    }
    m_receive_timestamp_buffer[m_timestamp_buffer_next_index++] = current_time;
}

void Print(const unsigned long current_time)
{
    if (current_time < m_last_check + INTERVAL)
    {
        return;
    }

    // Time to log
    PrintFrequency();

    if (m_timestamp_buffer_next_index < 2)
    {
        Serial.println("Less than two messages received. Not printing average latency.");
        // Clean up
        ResetMonitor(current_time);
        return;
    }
    const auto average_latency = GetAverageLatency();
    PrintAverageLatency(average_latency);

    // Clean up
    ResetMonitor(current_time);
}

private:

void PrintFrequency() const
{
    Serial.print(m_receive_count / ((float)INTERVAL/ 1000));
    Serial.print(' ');
}

void PrintAverageLatency(const unsigned long average_latency) const
{
    Serial.print(average_latency);
    Serial.println();
}

unsigned long GetAverageLatency() const
{
    unsigned long total = 0;
    for (unsigned int i = 0; i < m_timestamp_buffer_next_index - 1; i++)
    {
        total += m_receive_timestamp_buffer[i + 1] - m_receive_timestamp_buffer[i];
    }
    return total / (m_timestamp_buffer_next_index - 1);
}

void ResetMonitor(const unsigned long current_time)
{
    m_last_check = current_time;
    m_receive_count = 0;
    m_timestamp_buffer_next_index = 0;
}

const uint32_t INTERVAL;
unsigned long m_last_check;
unsigned long m_receive_count;
unsigned long* m_receive_timestamp_buffer;
unsigned int m_timestamp_buffer_size;
unsigned int m_timestamp_buffer_next_index;
};

class CANMessageReceiveBlackHole
{
public:
CANMessageReceiveBlackHole():
    m_len{0}
{}

// Return true if a command message from the VCU is received.
bool VCUCommandMessageReceived()
{
    if (CAN_MSGAVAIL == CAN.checkReceive())   // check if data coming
    {
        CAN.readMsgBuf(&m_len, m_buf);   // remove data from the buffer.
        const auto id = CAN.getCanId();
        if (id == 0x0C0)
        {
            return true;
        }
    }

    return false;
}

private:
unsigned char m_len = 0;
unsigned char m_buf[8];
};

class CANMessageFloodTransmitHelper
{
public:
CANMessageFloodTransmitHelper(const uint32_t pong_can_id, const uint32_t interval_ms, const unsigned int messages_per_interval):
    PONG_CAN_ID{pong_can_id},
    INTERVAL{interval_ms},
    MSG_PER_INTERVAL{messages_per_interval},
    m_last_check{0}
{}

Transmit(const unsigned long current_time)
{
    if (current_time >= m_last_check + INTERVAL)
    {
        for (unsigned int i = 0; i < MSG_PER_INTERVAL; i++)
        {
          CAN.sendMsgBuf(PONG_CAN_ID, 0, 8, buf);
        }
        m_last_check = current_time;
    }
}

private:
const uint32_t PONG_CAN_ID;
const uint32_t INTERVAL;
const unsigned int MSG_PER_INTERVAL;
uint32_t m_last_check;
unsigned char buf[8]; // Garbage value is okay. we won't need to transmit meaningful data.
};

const uint32_t PONG_CAN_ID = 0x0D0;
const uint32_t flood_interval_ms = 1;
const unsigned int flood_messages_per_interval = 0;

CANMessageFloodTransmitHelper canMsgTxHelper(PONG_CAN_ID, flood_interval_ms, flood_messages_per_interval);

const uint32_t performance_print_interval_ms = 500;
const unsigned int performance_monitor_buffer_size = 200;

PerformanceMonitor performanceMonitor(performance_print_interval_ms, performance_monitor_buffer_size);
CANMessageReceiveBlackHole canMsgRxBlackhole;

void setup()
{
    Serial.println("Observor initializing...");
    Serial.begin(115200);

    while( CAN.begin(CAN_500KBPS) ){   // init can bus : baudrate = 500k
        Serial.println("DFROBOT's CAN BUS Shield init fail");
        Serial.println("Please Init CAN BUS Shield again");
        delay(3000);
    }
    Serial.println("DFROBOT's CAN BUS Shield init ok!\n");

}

void loop()
{
    const auto current_time = millis();
    if (canMsgRxBlackhole.VCUCommandMessageReceived())
    {
        performanceMonitor.AddCount(1);
        performanceMonitor.RecordReceiveTime(current_time);   }
    
    performanceMonitor.Print(current_time);
    canMsgTxHelper.Transmit(current_time);
}