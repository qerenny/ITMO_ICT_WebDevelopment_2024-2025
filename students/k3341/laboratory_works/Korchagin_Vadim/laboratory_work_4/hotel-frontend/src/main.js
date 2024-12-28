import { createApp } from 'vue'
import App from './App.vue'

import router from './router'

import 'vuetify/styles'

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const myHotelTheme = {
  dark: false,  // светлая тема
  colors: {
    background: '#FFFFFF',
    surface: '#F5F5F5',        // светлый оттенок для фона карточек
    primary: '#4A90E2',        // приятный синий
    'primary-darken-1': '#357ABD',
    secondary: '#7BDCB5',      // мягкий зелёный
    'secondary-darken-1': '#57C09C',
    error: '#D32F2F',          // яркий красный для ошибок
    info: '#2D9CDB',           // небесно-голубой для информационных сообщений
    success: '#27AE60',        // зеленый успех
    warning: '#F2C94C',        // желтоватый для предупреждений
    // Можно добавить что-то типа «accent» или «tertiary», если нужно
  },
  // Дополнительные переменные, если хочется настроить отступы, прозрачность и т.д.
  variables: {
    'border-color': '#000000', 
    'border-opacity': 0.12,
  }
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'myHotelTheme',
    themes: {
      myHotelTheme
    }
  }
})

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')