#include <GyverTimers.h>

// Информация о прошивке
#define version_ (0 << 8) + 1 // мажор, минор версии
#define last_update 20221027 // дата последнего обновления


#define pin_ttl_out 4 // номер пин программного ШИМ
#define pin_led_out 13 // пин LED

#define timer_frequency 50000 // частота таймера, Гц (макс следование импульсов freq/2)


struct {
  uint8_t min_length = 4; // минимальная длина сообщения
  enum {READ, WRITE} operation; // индексы операций
  enum {
    OK,
    INVALID_OPERATION,
    INVALID_ADDRESS
  } response; // коды ответов(ошибок)
} uart_format; // формат сообщений UART


struct {

  enum {OFF, SINGLE, PERIODIC} regime = OFF; // режим работы лазера
  uint32_t pulse_width = 1; // ширина импульса
  uint32_t pulse_period = 0.02 * timer_frequency - 1; //  50 Гц. -1 т.к. есть такт между pulse_period и 0

} state;

volatile uint32_t timer_ticks = 0; // счетчик прерываний таймера


void setup()
{

    Timer2.setFrequency(timer_frequency); // устанавить частоту таймера
    Timer2.enableISR(); // включаем прерывания таймера 2
    
    pinMode(pin_ttl_out, OUTPUT); // инициализируем пин ШИМ сигнала
    pinMode(pin_led_out, OUTPUT); // инициализируем пин LED
    
    Serial.begin(9600); // частота UART (baudrate)
    Serial.setTimeout(250);
    
}


void loop() {
  ledControl();
  rxUart();
}


void rxUart() {
  if (Serial.available() >= uart_format.min_length) {
    Serial.flush();

    uint8_t rx_response = Serial.read();
    uint8_t rx_address = Serial.read();
    uint8_t rx_operation = Serial.read();
    uint8_t rx_data_length = Serial.read();

    if (rx_operation == uart_format.READ) {
      // readMemory
    } else if (rx_operation == uart_format.WRITE) {
      uint8_t rx_data[rx_data_length];
      Serial.readBytes(rx_data, rx_data_length);
      // writeMemory
    } else {
      uint8_t data[0] = {};
      txUart(uart_format.INVALID_OPERATION, rx_address, rx_operation, 0, data);
    }
    
  }
}


void readMemory(uint8_t address) {

  uint8_t *data;

  switch (address) {
    
    case 0x03: // версия прошивки
      data = new uint8_t[4];
      for (uint8_t i = 0; i < 4; i++) {
        data[i] = version_ >> 8*(3-i) & 0xff;
      }
      break;
    
    case 0x04: // дата последнего апдейта
      data = new uint8_t[4];
      for (uint8_t i = 0; i < 4; i++) {
        data[i] = last_update >> 8*(3-i) & 0xff;
      }
      break;

    case 0x05: // Частота таймера
      data = new uint8_t[4];
      for (uint8_t i = 0; i < 4; i++) {
        data[i] = timer_frequency >> 8*(3-i) & 0xff;
      }
      break;

    case 0x10: // режим работы лазера
      data = new uint8_t {state.regime};
      break;

    case 0x11: // период импульсов
      data = new uint8_t[4];
      for (uint8_t i = 0; i < 4; i++) {
        data[i] = (state.pulse_period + 1) >> 8*(3-i) & 0xff;
      }
      break;

    case 0x12: // ширина импульсов
      data = new uint8_t[4];
      for (uint8_t i = 0; i < 4; i++) {
        data[i] = state.pulse_width >> 8*(3-i) & 0xff;
      }
      break;

    default: // ошибка чтения адреса
      data = new uint8_t[0];
      break;
    
  }

  txUart(uart_format.OK, address, uart_format.READ, sizeof(data), data);
  
}


void writeMemory(uint8_t address, uint8_t data_length, uint8_t *data) {

  switch (address) {

    case 0x10: // режим работы лазера
      state.regime = data[0];
      break;

    case 0x11: // период импульсов
      state.pulse_period = 0;
      for (uint8_t i = 0; i < 4; i++) {
        state.pulse_period += data[i] << (3 - i) * 8;
      }

    case 0x12: // ширина импульсов
      state.pulse_width = 0;
      for (uint8_t i = 0; i < 4; i++) {
        state.pulse_width += data[i] << (3 - i) * 8;
      }

    default: // ошибка адреса записи
      break;
    
  }

  txUart(uart_format.OK, address, uart_format.WRITE, 0, {});
  
}


void txUart(
  uint8_t response,
  uint8_t address,
  uint8_t operation,
  uint8_t data_length,
  uint8_t *data
  ) {
    
  uint8_t message[uart_format.min_length + data_length];
  message[0] = response;
  message[1] = address;
  message[2] = operation;
  message[3] = data_length;

  for (uint8_t i=0; i < data_length; i++) {
    message[uart_format.min_length + i] = data[i];
  }

  Serial.write(message, sizeof(message));
  
}
//
//
//void timerTick() {
//  
//
// if (timer_ticks == state.pulse_start && state.regime != state.OFF && state.laser_enabled) {
//    digitalWriteFast(pin_ttl_out, HIGH);
// } else if (timer_ticks == state.pulse_end) {
//    digitalWriteFast(pin_ttl_out, LOW);
//    if (state.regime == state.SINGLE | state.regime == state.SINGLE_SYNC) {
//      state.laser_enabled = false;
//    }
// } else if (timer_ticks == state.pulse_period) {
//    timer_ticks = 0;
//    timer_ticks--;
//    state.synced = false;
// } else if (state.regime == state.OFF && !state.laser_enabled) {
//    digitalWriteFast(pin_ttl_out, LOW);
// }
// 
// timer_ticks++;
//
//}
//
//
//ISR(TIMER2_A) {
//  timerTick();
//}
//
//
//void syncTrigger() {
//
// timer_ticks = 0;
// sync_ticks_led++;
// state.synced = true;
//
//}
//
//
void ledControl() {

    if (timer_ticks){
      digitalWriteFast(pin_led_out, LOW);
    } else {
      digitalWriteFast(pin_led_out, HIGH);
    }

}


void digitalWriteFast(uint8_t pin, bool x) {
  if (pin < 8) {
    bitWrite(PORTD, pin, x);
  } else if (pin < 14) {
    bitWrite(PORTB, (pin - 8), x);
  } else if (pin < 20) {
    bitWrite(PORTC, (pin - 14), x);
  }
}
