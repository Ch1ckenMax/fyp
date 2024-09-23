#pragma once

#include <stdio.h>
#include <stm32f1xx.h>

namespace Tests
{

class ManualTests
{
public:
	void Run();

private:
	void ReadMemory(uint32_t startAddress, uint32_t length);

};

};
