<template>
  <div>
    <h2>Main Page</h2>
    <div v-if="loadingVariantgroup">Loading Variant Group status ...</div>
    <div class="mt-3" v-else-if="variantgroupStatus">
      Variant Groups with Variable: {{ variantgroupStatus.count - variantgroupStatus.withoutVariableCount }} / {{ variantgroupStatus.count }}
      <div v-if="variantgroupStatus.withoutVariableCount > 0">
        <v-btn color="primary" @click="checkVariantgroup" :loading="loadingVariantgroupCheck">Check & Repair</v-btn>
        <div v-if="variantgroupCheck">
          Without Variables: {{ variantgroupCheck.filter(c => c.variables.length === 0).length }}<br>
          More than one Variables: {{ variantgroupCheck.filter(c => c.variables.length > 1).length }}<br>
          <br>
          First 100 Entries:<br>
        </div>
        <ul class="mt-2" v-if="variantgroupCheck">
          <li v-for="aVG in variantgroupCheck" :key="aVG.id">
            {{ aVG.name }} - ID: {{ aVG.id }} - Variables:
            <span v-for="(aVar, aVarDg) in aVG.variables" :key="aVar.id">{{ aVarDg > 0 ? ', ' : '' }}<i>{{ aVar.name }}</i> - ID: {{ aVar.id }}</span>
            <b class="red--text" v-if="aVG.variables.length === 0">None!</b>
            <span v-if="aVG.variables.length > 1"> - <b class="orange--text">More than one!</b></span>
            <span v-if="aVG.repaired"> - <b class="green--text">Repaired</b></span>
            <!-- {{ aVG }} -->
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      loadingVariantgroup: false,
      variantgroupStatus: null,
      loadingVariantgroupCheck: false,
      variantgroupCheck: null
    }
  },
  mounted () {
    this.getVariantgroup()
  },
  methods: {
    checkVariantgroup () {
      this.loadingVariantgroupCheck = true
      this.$http
        .post('/system/', { get: 'variantgroup', check: true }, { headers: {'X-CSRFToken': this.csrf}, emulateJSON: true })
        .then((response) => {
          console.log(response.data)
          this.variantgroupStatus = response.data.variantgroup
          this.variantgroupCheck = response.data.check
          this.loadingVariantgroupCheck = false
        })
        .catch((err) => {
          console.log(err)
          this.loadingVariantgroupCheck = false
        })
    },
    getVariantgroup () {
      this.loadingVariantgroup = true
      this.$http
        .post('/system/', { get: 'variantgroup' }, { headers: {'X-CSRFToken': this.csrf}, emulateJSON: true })
        .then((response) => {
          console.log(response.data)
          this.variantgroupStatus = response.data.variantgroup
          this.loadingVariantgroup = false
        })
        .catch((err) => {
          console.log(err)
          this.loadingVariantgroup = false
        })
    }
  }
}
</script>

<style scoped>
</style>
