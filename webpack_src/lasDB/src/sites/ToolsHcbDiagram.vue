<template>
  <div id="toolshcbdiagram" class="h-100">
    <HcbDiagram :dbModels="diagramData" ref="diagram" v-if="diagramData" />
    <div id="toolbtns" v-if="diagramData">
      <v-btn fab dark small color="primary" class="mx-1"
        @click="$refs.diagram.fitWorkspace()"><v-icon dark>home</v-icon></v-btn>
      <v-btn fab dark small color="pink" class="mx-1"
        @click="saveDiagramData"><v-icon dark>save</v-icon></v-btn>
    </div>
  </div>
</template>

<script>
import HcbDiagram from '../components/HcbDiagram.vue'

export default {
  name: 'ToolsHcbDiagram',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      loading: true,
      diagramData: null
    }
  },
  mounted () {
    this.loadDiagramData()
  },
  methods: {
    loadDiagramData () {
      this.loading = true
      this.diagramData = null
      this.$http
        .post('/tools/diagram/', {
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          this.diagramData = response.data
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    },
    saveDiagramData () {
      if (this.diagramData) {
        this.loading = true
        this.$http
          .post('/tools/diagram/', {
            save: JSON.stringify(this.diagramData)
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            this.diagramData = null
            this.$nextTick(() => {
              this.diagramData = response.data
              this.loading = false
            })
          })
          .catch((err) => {
            console.log(err)
            this.loading = false
          })
      }
    }
  },
  components: {
    HcbDiagram
  }
}
</script>

<style scoped>
  #toolshcbdiagram {
    position: relative;
    box-shadow: 1px 1px 7px rgba(0,0,0,0.25);
    background: #eeeeee;
  }
  #toolbtns {
    position: absolute;
    right: 0;
    top: 0;
  }
</style>
