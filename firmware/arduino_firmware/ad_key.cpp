
#include "ad_key.h"

// ADKey 按键电压分区（示例，需根据实际电路调整）
// ADKEY_NUM_KEYS=5，则应有6个分界点
const int ADKey::keyThresholds[ADKEY_NUM_KEYS+1] = { 0, 400, 800, 1200, 1600, 4096 };

ADKey::ADKey(uint8_t pin) : _pin(pin) {}

void ADKey::begin() {
    pinMode(_pin, INPUT);
}

int ADKey::readRaw() {
    return analogRead(_pin);
}

int ADKey::getKey() {
    int value = readRaw();
    return 0;
}
