#include <Arduino.h>
#include "RampsStepper.h"
#include "logger.h"

RampsStepper::RampsStepper(int aStepPin, int aDirPin, int aEnablePin, bool aInverse, float main_gear_teeth, float motor_gear_teeth, int microsteps, int steps_per_rev) {
  setReductionRatio(main_gear_teeth / motor_gear_teeth, microsteps * steps_per_rev);
  stepPin = aStepPin;
  dirPin = aDirPin;
  enablePin = aEnablePin;
  inverse = aInverse;
  stepperStepPosition = 0;
  stepperStepTargetPosition;
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  enable(false);
}

void RampsStepper::enable(bool value) {
  digitalWrite(enablePin, !value);
}

bool RampsStepper::isOnPosition() const {
  return stepperStepPosition == stepperStepTargetPosition;
}

int RampsStepper::getPosition() const {
  return stepperStepPosition;
}

void RampsStepper::setPosition(int value) {
  stepperStepPosition = value;
  stepperStepTargetPosition = value;
}

void RampsStepper::stepToPosition(int value) {
  stepperStepTargetPosition = value;
}

void RampsStepper::stepToPositionMM(float mm, float steps_per_mm) {
  stepperStepTargetPosition = mm * steps_per_mm;
}

void RampsStepper::stepRelative(int value) {
  value += stepperStepPosition;
  stepToPosition(value);
}

float RampsStepper::getPositionRad() const {
  return stepperStepPosition / radToStepFactor;
}

void RampsStepper::setPositionRad(float rad) {
  setPosition(rad * radToStepFactor);
}

void RampsStepper::stepToPositionRad(float rad) {
  stepperStepTargetPosition = rad * radToStepFactor;
}

void RampsStepper::stepRelativeRad(float rad) {
  stepRelative(rad * radToStepFactor);
}

// int i = 0;

void RampsStepper::update() {   
  while (stepperStepTargetPosition < stepperStepPosition) {  
    digitalWrite(dirPin, !inverse);
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin, LOW);
    stepperStepPosition--;
  }
  
  while (stepperStepTargetPosition > stepperStepPosition) {    
    digitalWrite(dirPin, inverse);
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin, LOW);
    stepperStepPosition++;
  }

  // if (stepperStepTargetPosition == stepperStepPosition)
  // {
  //   Serial.print(F("MOVE COMPLETE\r\n"));
  // }
}

void RampsStepper::setReductionRatio(float gearRatio, int stepsPerRev) {
  radToStepFactor = gearRatio * stepsPerRev / 2 / PI;
};
