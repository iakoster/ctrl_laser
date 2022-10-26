#include <GyverTimers.h>

// Информация о прошивке
#define ver_global 0 // Глобальная версия
#define ver_major 0 // Мажор версия
#define ver_minor 1 // Минор версия
#define ver_patch 0 // Патч версия
#define last_update (2022 << 16) + (10 << 8) + 26 // Дата последнего обновления


#define pin_ttl_out 4 // Номер пин программного ШИМ
#define pin_led_out 13 // Пин LED
#define led_blink_multiplier 49 // Сколько нужно импульсов для морграния светодиода

#define timer_frequency 50000 // частота таймера, Гц (макс следование импульсов freq/2)


struct {
  uint8_t min_length = 5; // минимальная длина сообщения
  enum {READ, WRITE} operation; // индексы операций
} uart_format; // Формат сообщений UART


struct {

  enum {OFF, SINGLE, PERIODIC} regime = OFF; // Режим работы лазера
  uint16_t pulse_offset = 0; // Смещение импульса
  uint16_t pulse_width = 1; // Ширина импульса
  uint16_t pulse_start = 0; // Старт импульса
  uint16_t pulse_end = 1; // Конец импульса
  uint16_t pulse_period = 0.02 * timer_frequency - 1; //  50 Гц (при 50кГц таймере). Меньше на 1 т.к. есть такт между 999 и 0

} state;

volatile uint16_t timer_ticks = 0; // Счетчик прерываний таймера


void setup()
{

    Timer2.setFrequency(timer_frequency); // Устанавить частоту таймера
    Timer2.enableISR(); // Включаем прерывания таймера 2
    
    pinMode(pin_ttl_out, OUTPUT); // Инициализируем пин ШИМ сигнала
    pinMode(pin_led_out, OUTPUT); // Инициализируем пин LED
    
    Serial.begin(9600); // Частота UART (baudrate)
    Serial.setTimeout(250);
    
}


void loop() {
  ledControl();
  //rxUart();
}
//
//
//void rxUart() {
//
//    if (Serial.available() >= uart_format.min_length)
//  {
//    Serial.flush();
//    uint16_t rx_preamble = (Serial.read() << 8) + Serial.read();
//    if (rx_preamble != uart_format.preamble) { 
//      uint8_t data[1] = {0x10}; // preamble error
//      txUart(0x00, uart_format.ANSWER_ERROR, 1, data);
//      delete data;
//      return;
//    }
//
//    uint8_t rx_address = Serial.read();
//    uint8_t rx_operation = Serial.read();
//    uint8_t rx_data_len = Serial.read();
//
//    if (rx_operation == uart_format.RX_READ) {
//      readMemory(rx_address);
//    } else if (rx_operation == uart_format.RX_WRITE) {
//      uint8_t rx_data[rx_data_len];
//      Serial.readBytes(rx_data, rx_data_len);
//      writeMemory(rx_address, rx_data_len, rx_data);
//    } else {
//      uint8_t data[1] = {0x11}; // operation error
//      txUart(rx_address, uart_format.ANSWER_ERROR, 1, data);
//      delete data;
//    }
//    
//  }
//
//}
//
//
//void writeMemory(uint8_t address, uint16_t data_len, uint8_t *data) {
//
//  uint8_t operation = uart_format.ANSWER_WRITE;
//
//  switch (address)
//  {
//  
//  case 0x0e: // Вкл/выкл лазер
//    state.laser_enabled = data[0];
//    break;
//
//  case 0x10: // режим работы лазера
//    state.regime = data[0];
//    break;
//  
//  case 0x11: // смещение импульса относительно начала периода
//    state.pulse_offset = (data[0] << 8) + data[1];
//    updatePulseStartEnd();
//    break;
//
//  case 0x12: // ширина импульса
//    state.pulse_width = (data[0] << 8) + data[1];
//    updatePulseStartEnd();
//    break;
//
//  case 0x13: // период импульсов
//    state.pulse_period = (data[0] << 8) + data[1] - 1;
//    updatePulseStartEnd();
//    break;
//  
//  default: // ошибка адреса записи
//    data = new uint8_t[1] {0x12};
//    data_len = 1;
//    operation = uart_format.ANSWER_ERROR;
//    break;
//  }
//
//  txUart(address, operation, data_len, data);
//
//}
//
//void updatePulseStartEnd() {
//  state.pulse_start = state.pulse_offset;
//  state.pulse_end = (state.pulse_offset + state.pulse_width) % (state.pulse_period + 1);
//}
//
//
//void readMemory(uint8_t address) {
//
//  uint8_t operation = uart_format.ANSWER_READ;
//  uint8_t *data;
//  uint8_t data_len;
//
//  switch (address)
//  {
//  
//  case 0x03: // Версия прошивки
//    data = new uint8_t[4] {ver_global, ver_major, ver_minor, ver_patch};
//    data_len = 4;
//    break;
//
//  case 0x04: // Дата последнего апдейта
//    data = new uint8_t[4];
//    for (uint8_t i = 0; i < 4; i++) {
//      data[i] = last_update >> 8*(3-i) & 0xff;
//    }
//    data_len = 4;
//    break;
//
//  case 0x05: // Частота таймера
//    data = new uint8_t[4];
//    for (uint8_t i = 0; i < 4; i++) {
//      data[i] = timer_frequency >> 8*(3-i) & 0xff;
//    }
//    data_len = 4;
//    break;
//  
//  case 0x06: // Наличие синхронизации
//    data = new uint8_t[1] {state.synced};
//    data_len = 1;
//    break;
//  
//  case 0x0e: // Вкл/выкл лазер
//    data = new uint8_t[1] {state.laser_enabled};
//    data_len = 1;
//    break;
//
//  case 0x10: // режим работы лазера
//    data = new uint8_t[1] {state.regime};
//    data_len = 1;
//    break;
//
//  case 0x11: // смещение импульса относительно начала периода
//    data = new uint8_t[2] {state.pulse_offset >> 8, state.pulse_offset & 0xff};
//    data_len = 2;
//    break;
//  
//  case 0x12: // ширина импульса
//    data = new uint8_t[2] {state.pulse_width >> 8, state.pulse_width & 0xff};
//    data_len = 2;
//    break;
//
//  case 0x13: // период импульсов
//    data = new uint8_t[2] {(state.pulse_period + 1) >> 8, (state.pulse_period + 1) & 0xff};
//    data_len = 2;
//    break;
//  
//  case 0x14: // старт и конец импульса
//    data = new uint8_t[4] {state.pulse_start >> 8, state.pulse_start & 0xff,
//                           state.pulse_end >> 8, state.pulse_end & 0xff};
//    data_len = 4;
//    break;
//  
//  default: // ошибка адреса чтения
//    data = new uint8_t[1] {0x12};
//    data_len = 1;
//    operation = uart_format.ANSWER_ERROR;
//    break;
//
//  }
//
//  txUart(address, operation, data_len, data);
//
//}
//
//void txUart(uint8_t address, uint8_t operation, uint8_t data_len, uint8_t *data) {
//
//  uint8_t message[data_len + uart_format.min_length];
//  message[0] = uart_format.preamble >> 8;
//  message[1] = uart_format.preamble & 0xff;
//
//  message[2] = address;
//  message[3] = operation;
//  message[4] = data_len;
//  for (uint8_t i=0; i < data_len; i++) {
//    message[i + uart_format.min_length] = data[i];
//  }
//
//  Serial.write(message, sizeof(message));
//
//}
//
//// uint8_t *uint2Bytes(uint64_t var, uint8_t bytes_count) {
////   uint8_t bytes[bytes_count];
////   for (uint8_t i = 0; i < bytes_count; i++) {
////     bytes[i] = var & 0xff;
////     var = var >> 8;
////   }
////   return bytes;
//
//// }
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
