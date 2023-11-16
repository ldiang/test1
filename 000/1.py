<template>
  <div>
    <label for="cityInput">城市名称：</label>
    <input type="text" id="cityInput" v-model="cityName" @input="translateCity" />
    <p>英文名称：{{ translatedCity.en }}</p>
    <p>中文名称：{{ translatedCity.cn }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cityName: '',
      translatedCity: {
        en: '',
        cn: ''
      }
    };
  },
  methods: {
    // 调用翻译API的函数，这里使用了假设的翻译函数
    translate(cityName) {
      // 在实际应用中，你需要调用真实的翻译API
      // 这里仅作为演示目的，你需要替换成真实的API调用
      // 例如，可以使用axios库发送HTTP请求到翻译API

      // 假设这里是一个翻译函数
      return {
        en: `Translated_${cityName}`, // 用你的翻译结果替换这里
        cn: cityName
      };
    },
    translateCity() {
      const translated = this.translate(this.cityName);
      this.translatedCity.en = translated.en;
      this.translatedCity.cn = translated.cn;
    }
  }
};
</script>





