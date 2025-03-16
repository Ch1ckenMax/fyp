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
PerformanceMonitor(const uint32_t print_interval):
    INTERVAL{print_interval},
    m_last_check{0},
    m_receive_count{0}
{}

void CheckMessageReceived()
{
  if (CAN_MSGAVAIL == CAN.checkReceive())   // check if data coming
  {
      CAN.readMsgBuf(&m_len, m_buf);   // remove data from the buffer.
      const auto id = CAN.getCanId();
      if (id == 0x0C0) m_receive_count += 1;
  }
}

void Print(const unsigned long current_time)
{
    if (current_time < m_last_check + INTERVAL) return;
    PrintFrequency(); // Time to log
    ResetMonitor(current_time); // Clean up
}

private:

void PrintFrequency() const
{
    Serial.print(m_receive_count / ((float)INTERVAL/ 1000));
    Serial.println(' ');
}

void ResetMonitor(const unsigned long current_time)
{
    m_last_check = current_time;
    m_receive_count = 0;
}

const uint32_t INTERVAL;
unsigned long m_last_check;
unsigned long m_receive_count;
unsigned char m_len = 0;
unsigned char m_buf[8];
};

class CANMessageFloodTransmitHelper
{
public:
CANMessageFloodTransmitHelper(const uint32_t pong_can_id, const unsigned int messages_per_interval):
    PONG_CAN_ID{pong_can_id},
    msg_per_interval{messages_per_interval},
    m_last_check{0},
    m_last_interval_increase{0}
{}

Transmit(const unsigned long current_time)
{
    if (current_time / 3000 != m_last_interval_increase)
    {
       msg_per_interval += 1;
       Serial.print("Interval is now increased to ");
       Serial.print(msg_per_interval);
       Serial.println();
       m_last_interval_increase = current_time / 3000;
    }

    if (current_time > m_last_check)
    {
        for (unsigned int i = 0; i < msg_per_interval; i++)
        {
          CAN.sendMsgBuf(PONG_CAN_ID, 0, 8, buf);
        }
        m_last_check = current_time;
    }
}

private:
const uint32_t PONG_CAN_ID;
unsigned int msg_per_interval;
uint32_t m_last_check;
uint32_t m_last_interval_increase;
unsigned char buf[8]; // Garbage value is okay. we won't need to transmit meaningful data.
};

const uint32_t PONG_CAN_ID = 0x0A5;
const unsigned int flood_messages_per_ms = 0;

CANMessageFloodTransmitHelper canMsgTxHelper(PONG_CAN_ID, flood_messages_per_ms);

const uint32_t performance_print_interval_ms = 500;
PerformanceMonitor performanceMonitor(performance_print_interval_ms);

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
    uint8_t buf[8];
    const uint32_t id = 0x0A5;
    CAN.sendMsgBuf(id, 0, 8, buf);

}

void loop()
{
    const auto current_time = millis();
    performanceMonitor.CheckMessageReceived();
    
    performanceMonitor.Print(current_time);
    canMsgTxHelper.Transmit(current_time);
}