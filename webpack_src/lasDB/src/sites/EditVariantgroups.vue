<template>
  <div class="h-100">
    <DBForm table="lex_variantgroup" form="lex_variantgroup" :user="user" :options="options" :csrf="csrf" ref="form">
      <template slot="extraBtns">
        <v-btn @click="exportXLS" color="primary" icon flat style="position:absolute;right:85px;top:10px;"><v-icon>mdi-file-excel-outline</v-icon></v-btn>
      </template>
    </DBForm>
    <v-dialog v-model="loading" persistent width="300">
      <v-card color="primary" dark>
        <v-card-text>
          Loading ... please stand by
          <v-progress-linear indeterminate color="white" class="mb-0" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import DBForm from '../components/DBForm.vue'
const ExcelJS = require('exceljs')

export default {
  name: 'EditVariantgroups',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      loading: false
    }
  },
  methods: {
    exportXLS () {
      if (this.$refs.form && this.$refs.form.contentID > 0) {
        console.log('exportXLS', this.$refs.form && this.$refs.form.contentID)
        this.loading = true
        this.$http
          .post('/export/', {
            get: 'variantgroups',
            id: this.$refs.form && this.$refs.form.contentID
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log('exportXLS', response.data)
            let aTime = new Date()
            let aDateTime = aTime.toLocaleString('en-US')
            const wb = new ExcelJS.Workbook()
            wb.title = 'Variant Groups/Variants'
            wb.subject = 'Variants'
            wb.creator = 'lasDB'
            wb.created = aTime
            var ws
            ws = wb.addWorksheet('Variants')
            ws.addRow([response.data.variantgroup.str])
            if (response.data.variantgroup.description) {
              ws.addRow([response.data.variantgroup.description])
            }
            if (response.data.variantgroup.comment) {
              ws.addRow([response.data.variantgroup.comment])
            }
            ws.addRow([aDateTime])
            ws.addRow()
            let aRow = ws.addRow(['Id', 'Variant', 'Group', 'Comment', 'Informant Count', 'District Count', 'Belong to Count'])
            ws.columns = [
              { key: 'id', width: 5 },
              { key: 'variant', width: 20 },
              { key: 'group', width: 30 },
              { key: 'comment', width: 30 },
              { key: 'infCount', width: 10 },
              { key: 'infDistCount', width: 10 },
              { key: 'infBelongCount', width: 10 }
            ]
            aRow.style = { font: { bold: true } }
            aRow.border = { bottom: { style: 'medium' } }
            aRow.eachCell(c => {
              c.style = { font: { bold: true } }
              c.border = { bottom: { style: 'medium' } }
            })
            response.data.variants.forEach(dRow => {
              ws.addRow([
                dRow.id,
                dRow.variant,
                dRow.group ? dRow.group.map(gRow => gRow.group.name + ' (' + gRow.group.id + ')').join(', ') : null,
                dRow.comment,
                dRow.infCount,
                dRow.infDistCount,
                dRow.infBelongCount
              ])
            })
            wb.xlsx.writeBuffer().then(this.saveFile.bind(null, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx', 'lasdb_vgv_' + response.data.variantgroup.id + '_' + aTime.getFullYear() + '-' + ('0' + aTime.getMonth()).slice(-2) + '-' + ('0' + aTime.getDay()).slice(-2) + '_' + ('0' + aTime.getHours()).slice(-2) + '-' + ('0' + aTime.getMinutes()).slice(-2) + '-' + ('0' + aTime.getSeconds()).slice(-2)))
            this.loading = false
          })
          .catch((err) => {
            console.log(err)
            this.loading = false
          })
      }
    },
    saveFile (mimeType, aFileType, aFilename, buffer) {
      if (buffer) {
        // console.log(buffer)
        if (buffer) {
          let blob = new Blob([buffer], {type: mimeType})
          const a = document.createElement('a')
          a.href = URL.createObjectURL(blob)
          a.download = aFilename + '.' + aFileType
          a.click()
        }
      } else {
        alert('Error on creating file!')
      }
    }
  },
  components: {
    DBForm
  }
}
</script>

<style scoped>
</style>
