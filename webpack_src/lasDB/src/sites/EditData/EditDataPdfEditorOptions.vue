<template>
  <v-card flat>
    <v-card-text>
      <v-subheader class="pl-0">Brightness</v-subheader>
      <v-slider v-model="selectedPdfFile.options.brightness" :max="3" :min="0.5" :step="0.05" :disabled="pdfImageTextL" thumb-label="always" prepend-icon="brightness_medium" append-icon="settings_backup_restore" @click:append="selectedPdfFile.options.brightness = defaultOptions.brightness"></v-slider>
      <v-subheader class="pl-0">Contrast</v-subheader>
      <v-slider v-model="selectedPdfFile.options.contrast" :max="3" :min="0.5" :step="0.05" :disabled="pdfImageTextL" thumb-label="always" prepend-icon="invert_colors" append-icon="settings_backup_restore" @click:append="selectedPdfFile.options.contrast = defaultOptions.contrast"></v-slider>
      <v-switch v-model="pdfImageTextL" :label="'Switch to ' + (pdfImageTextL ? 'Scan' : 'OCR-Text')"></v-switch>
      <v-text-field label="Title" v-model="selectedPdfFile.title"></v-text-field>
      <v-checkbox v-model="selectedPdfFile.edit_data" label="Edit Data"></v-checkbox>
      <v-textarea v-model="selectedPdfFile.comment" label="comment"></v-textarea>
      <v-btn @click="savePdfOptions" color="info" :loading="loading" :disabled="loading">Save PDF options</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'EditDataPdfEditorOptions',
  props: ['selectedPdfFile', 'pdfImageText', 'defaultOptions', 'user', 'options', 'csrf'],
  data () {
    return {
      pdfImageTextL: false,
      loading: false
    }
  },
  mounted () {
    this.pdfImageTextL = this.pdfImageText
  },
  methods: {
    savePdfOptions () {
      console.log('savePdfOptions', this.selectedPdfFile)
      this.loading = true
      this.$http
        .post('/editData/', {
          set: 'setPdfOptions',
          data: JSON.stringify(this.selectedPdfFile)
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    }
  },
  watch: {
    pdfImageText (nVal) {
      this.pdfImageTextL = nVal
    },
    pdfImageTextL (nVal) {
      if (nVal !== this.pdfImageText) {
        this.$emit('changePdfImageText', nVal)
      }
    }
  }
}
</script>

<style scoped>
</style>
