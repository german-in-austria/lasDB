<template>
  <div style="position: relative;" class="h-100">
    <div style="position: relative; overflow-y: auto;" class="h-100">
      <div class="dbformcontent-main">
        <div class="pt-2 px-4 pb-5 white mh100">
          <h2 class="mb-3">
            {{ tabledata.data.model.verbose_name }} - <b>{{ entryStr }}</b> ({{ contentID > 0 ? contentID : 'NEW' }})
            <v-btn @click="deleteElement" v-if="edit && contentID > 0" color="red" icon flat style="top:-4px;"><v-icon>delete_forever</v-icon></v-btn>
          </h2>
          <v-layout flex wrap v-if="values">
            <template v-for="(field, key) in tabledata.data.options.fields">
              <div v-if="field.nl" :key="'nl' + key" class="nl"></div>
              <DBFormContentField
                :tabledata="tabledata"
                :field="field"
                :edit="edit"
                :values="values"
                :csrf="csrf"
                :key="'f' + key"
              />
            </template>
          </v-layout>
        </div>
      </div>
    </div>
    <slot name="extraBtns" v-if="!edit" />
    <v-btn v-if="!edit && !blocked" @click="edit = true" color="primary" fab small dark style="position:absolute;right:30px;top:10px;"><v-icon>edit</v-icon></v-btn>
    <v-btn v-if="!edit" @click="$emit('close')" flat fab small style="position:absolute;right:0px;top:0px;width:20px;height:20px;"><v-icon>mdi-close</v-icon></v-btn>
    <div v-if="edit && !blocked" style="position:absolute;right:30px;bottom:10px;">
      <v-btn @click="discardChanges" title="Discard Changes" color="warning" fab small dark><v-icon>reply</v-icon></v-btn>
      <v-btn @click="saveChanges" title="Save Changes" color="success" fab small dark><v-icon>save_alt</v-icon></v-btn>
    </div>
    <!-- Overlay Buttons ("Reload/Delete/Save" right bottom) -->
    <v-dialog v-model="loading" hide-overlay persistent width="300">
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
import AllgemeineFunktionen from '@/functions/Allgemein'
import DBFormContentField from './DBFormContentField.vue'

export default {
  name: 'DBFormContent',
  props: ['user', 'options', 'csrf', 'tabledata', 'contentID', 'blocked', 'startEdit'],
  data () {
    return {
      loading: false,
      edit: false,
      values: null,
      entryStr: ''
    }
  },
  created () {
    this.resetValues()
  },
  mounted () {
    console.log('DBFormContent mounted ...')
    console.log(this.tabledata.data)
    console.log(this.values)
    if (this.contentID > 0) {
      this.getValues()
      this.edit = this.startEdit || false
    } else {
      this.edit = true
    }
    console.log(this.tabledata.data.options.fields)
  },
  methods: {
    deleteElement () {
      if (confirm('Datensatz wirklich endgültig löschen?')) {
        console.log('deleteElement', this.contentID)
        this.loading = true
        this.$http
          .post('/form/', {
            get: 'delContent',
            delContent: true,
            app: this.tabledata.data.model.app,
            model: this.tabledata.data.model.model,
            pk: this.contentID
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log(response.data)
            if (response.data.deleted) {
              this.$emit('contentUpdated', -1, this.sortFieldValue)
              this.$emit('close')
            } else {
              alert('Error while deleting!\n' + response.data.errors)
            }
            this.loading = false
          })
          .catch((err) => {
            console.log(err)
            this.edit = true
            this.loading = false
            alert('Error while saving!')
          })
      }
    },
    saveChanges () {
      let errors = false
      Object.keys(this.values).forEach(aKey => {
        console.log(aKey, this.values[aKey])
        if (this.values[aKey].fieldVue) {
          if (this.values[aKey].fieldVue.error) {
            errors = true
          }
        }
      })
      // Speichern
      if (!errors) {
        this.edit = false
        this.loading = true
        this.$http
          .post('/form/', {
            get: 'setContent',
            setValues: true,
            app: this.tabledata.data.model.app,
            model: this.tabledata.data.model.model,
            pk: this.contentID,
            data: JSON.stringify(AllgemeineFunktionen.removeSubProperties(this.values, ['fieldVue']))
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log(response.data)
            if (response.data.saved) {
              let oldSortFieldValue = this.sortFieldValue
              this.entryStr = response.data.entryStr
              this.values = response.data.values
              this.$emit('contentUpdated', this.values.id.val, this.sortFieldValue, oldSortFieldValue)
            } else {
              this.edit = true
              alert('Error while saving!\n' + response.data.errors)
            }
            this.loading = false
          })
          .catch((err) => {
            console.log(err)
            this.edit = true
            this.loading = false
            alert('Error while saving!')
          })
      } else {
        alert('Error! Please fill all needed fields!')
      }
    },
    discardChanges () {
      if (confirm('Discard changes?')) {
        if (this.startEdit) {
          this.$emit('close')
        } else {
          this.edit = false
          if (this.contentID > 0) {
            this.getValues()
          } else {
            this.$emit('close')
          }
        }
      }
    },
    getValues () {
      console.log('getValues')
      this.loading = true
      this.resetValues()
      this.$http
        .post('/form/', {
          get: 'getContent',
          getValues: true,
          app: this.tabledata.data.model.app,
          model: this.tabledata.data.model.model,
          pk: this.contentID
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log(response.data)
          this.entryStr = response.data.entryStr
          Object.keys(response.data.values).forEach(aFieldName => {
            if (this.values && this.values.hasOwnProperty(aFieldName)) {
              let tmp = this.values[aFieldName].fieldVue
              this.values[aFieldName] = response.data.values[aFieldName]
              this.values[aFieldName].fieldVue = tmp
            } else {
              this.values[aFieldName] = response.data.values[aFieldName]
            }
          })
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    },
    resetValues () {
      if (!this.values) {
        this.values = {}
        this.tabledata.data.options.fields.forEach(aField => {
          if (!this.values.hasOwnProperty(aField.field_name)) {
            this.$set(this.values, aField.field_name, { val: null })
          }
        })
      }
    },
    getFieldTitle (aField) {
      if (aField.verbose_name) {
        return aField.verbose_name
      }
      let aOrgField = AllgemeineFunktionen.getFirstObjectOfValueInPropertyOfArray(this.tabledata.data.model.fields, 'field_name', aField.field_name)
      if (aOrgField.verbose_name) {
        return aOrgField.verbose_name
      }
      return aField.field_name
    }
  },
  computed: {
    sortFieldName () {
      return this.tabledata.data.options.ordering[0] || this.tabledata.data.model.ordering[0]
    },
    sortField () {
      return AllgemeineFunktionen.getFirstObjectOfValueInPropertyOfArray(this.tabledata.data.model.fields, 'field_name', this.sortFieldName)
    },
    sortFieldValue () {
      if (this.values && this.values[this.sortFieldName]) {
        return this.values[this.sortFieldName].val
      }
      return null
    }
  },
  components: {
    DBFormContentField
  }
}
</script>

<style scoped>
.dbformcontent-main {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.mh100 {
  min-height: 100%;
}
.nl {
  width: 100%;
  height: 0px;
}
</style>
