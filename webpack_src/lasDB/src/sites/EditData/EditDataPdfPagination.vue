<template>
  <div>
    <v-btn @click="selectedPdfSite -= 1" color="white" small class="pbtn" :disabled="selectedPdfSite <= 1"><v-icon>chevron_left</v-icon></v-btn>
    <v-text-field type="number" @change="checkPage" v-model="selectedPdfSite" class="sfield" :hide-details="true" />
    / {{ selectedPdfFile.localData.maxPdfSite }}
    <v-btn @click="selectedPdfSite += 1" color="white" small class="pbtn" :disabled="selectedPdfSite > selectedPdfFile.localData.maxPdfSite - 1"><v-icon>chevron_right</v-icon></v-btn>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'EditDataPdfPagination',
  props: ['selectedPdfFile', 'user', 'options', 'csrf'],
  data () {
    return {
      selectedPdfSite: 1
    }
  },
  mounted () {
    this.selectedPdfSite = this.selectedPdfFile.localData.selectedPdfSite
  },
  methods: {
    checkPage: _.debounce(function () {
      this.selectedPdfSite = parseInt(this.selectedPdfSite)
      if (this.selectedPdfSite < 1 || isNaN(this.selectedPdfSite)) {
        this.selectedPdfSite = 1
      }
      if (this.selectedPdfSite > this.selectedPdfFile.localData.maxPdfSite) {
        this.selectedPdfSite = this.selectedPdfFile.localData.maxPdfSite
      }
      this.changePage()
    }, 20),
    changePage: _.debounce(function () {
      this.selectedPdfFile.localData.selectedPdfSite = this.selectedPdfSite
    }, 250)
  },
  watch: {
    'selectedPdfSite' () {
      this.checkPage()
    }
  }
}
</script>

<style scoped>
.pbtn {
  min-width: 0;
  padding: 0 3px;
}
.sfield {
  padding-top: 0;
  max-width: 30px;
  display: inline-flex;
}
.sfield >>> input {
  -moz-appearance: textfield;
  text-align: right;
}
.sfield >>> input::-webkit-outer-spin-button,
.sfield >>> input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
