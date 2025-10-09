#ifndef AD_KEY_H
#define AD_KEY_H

#include <Arduino.h>

#define ADKEY_NUM_KEYS 5 // 按实际按键数量调整

class ADKey {
public:
    ADKey(uint8_t pin);
    void begin(); // 初始化
    int readRaw(); // 读取原始AD值
    int getKey();  // 获取按键编号（0~N-1），无按键返回-1
    static const int keyThresholds[ADKEY_NUM_KEYS+1];
private:
    uint8_t _pin;
};

#endif // ADKEY_H
