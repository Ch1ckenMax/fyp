#include <ManualTests.hpp>

namespace Tests
{

void ManualTests::Run()
{
	ReadMemory(0x08000000, 8);
}

void ManualTests::ReadMemory(uint32_t startAddress, uint32_t length)
{
	printf("Read Memory: ");

	uint8_t *startPtr = (uint8_t *)startAddress;

	for (uint32_t index = 0; index < length; index++)
	{
		printf("%02x ", *(startPtr + sizeof(uint8_t) * index));
	}

	printf("\n");
}

};




