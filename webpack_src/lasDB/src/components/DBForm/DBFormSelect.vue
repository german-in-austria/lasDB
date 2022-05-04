<template>
  <div style="position: relative; overflow-y: auto;" class="h-100" @scroll="listContentLoadCheck">
    <div class="dbformsel-main px-1">
      <div class="cont pt-1 pb-5">
        <DBFormSelectSearch @searchIt="searchIt" :tabledata="tabledata" :options="options" :csrf="csrf" :loading="loading" v-if="tabledata.data.model.search_fields && tabledata.data.model.search_fields.length > 0" />
        <DBFormSelectFilter @filterIt="filterIt" :tabledata="tabledata" :options="options" :csrf="csrf" v-if="tabledata.data.model.filter_fields && tabledata.data.model.filter_fields.length > 0" />
        <div
          v-for="list in lists"
          :key="'ml-' + list.filter"
          :class="'sel-l' + (list.open ? ' active' : '')"
        >
          <button
            class="btn-l"
            @click="toggleContentShow(list)"
            ><b>{{ list.name }}</b><i>{{ list.count > -1 ? list.count : '?' }}</i><v-progress-circular v-if="loading && list.loading" class="sel-l-loading mr-2" indeterminate size="16" width="2" color="primary" /></button>
          <div v-if="list.open">
            <div
              v-for="content in list.content"
              :key="'ml-' + content.id"
              :class="'sel-c' + (content.id === contentID ? ' active' : '')"
            >
              <button
                class="btn-cl"
                :title="'ID: ' + content.id"
                @click="loadContent(content.id)"
                >{{ content.title }}<v-icon v-if="content.id === contentID" class="sel-c-icon">chevron_right</v-icon></button>
            </div>
            <div ref="lcLoad" class="lc-load text-xs-center" :data-list-item="list.filter" v-if="!list.loaded">
              <v-progress-circular v-if="loading && list.loading" indeterminate size="24" color="primary" />
              <v-icon v-else>timer</v-icon>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import AllgemeineFunktionen from '@/functions/Allgemein'
import DBFormSelectSearch from './DBFormSelect/DBFormSelectSearch'
import DBFormSelectFilter from './DBFormSelect/DBFormSelectFilter'

export default {
  name: 'DBFormSelect',
  props: ['user', 'options', 'csrf', 'tabledata', 'contentID'],
  data () {
    return {
      loading: false,
      lists: [],
      searchObj: { val: '' },
      filterObj: {}
    }
  },
  mounted () {
    console.log('DBFormSelect mounted ...')
    this.getSelectList()
  },
  methods: {
    searchIt (sVal) {
      console.log('searchIt', sVal)
      this.searchObj = sVal
      this.getSelectList(true)
    },
    filterIt (val) {
      console.log('filterIt', val)
      this.filterObj[val.field] = val.val
      this.getSelectList(true)
    },
    loadContent (aId) {
      this.$emit('loadcontent', aId)
    },
    contentUpdated (id, sortFieldValue, oldSortFieldValue, isNewId) {
      console.log('contentUpdate', id, sortFieldValue, oldSortFieldValue, isNewId)
      this.getSelectList(true, id)
    },
    getSelectList (update = false, id = -1) {
      console.log('getSelectList', this.tabledata.data.model.app, this.tabledata.data.model.model, this.sortField.field_name, this.searchObj)
      this.loading = true
      this.$http
        .post('/form/', {
          get: 'getSelect',
          getLists: true,
          app: this.tabledata.data.model.app,
          model: this.tabledata.data.model.model,
          field: this.sortField.field_name,
          searchObj: JSON.stringify(this.searchObj),
          filterObj: JSON.stringify(this.filterObj),
          id: id
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log(response.data, update)
          this.lists = response.data.selectLists
          this.loading = false
          this.listContentLoadCheck()
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    },
    toggleContentShow (aList) {
      aList.open = !aList.open
      this.listContentLoadCheck()
    },
    getSelectListCont (aListName) {
      if (!this.loading) {
        let aList = AllgemeineFunktionen.getFirstObjectOfValueInPropertyOfArray(this.lists, 'filter', aListName)
        console.log('getSelectListCont', aListName, aList)
        this.loading = true
        aList.loading = true
        this.$http
          .post('/form/', {
            get: 'getSelect',
            getList: true,
            app: this.tabledata.data.model.app,
            model: this.tabledata.data.model.model,
            field: this.sortField.field_name,
            searchObj: JSON.stringify(this.searchObj),
            filterObj: JSON.stringify(this.filterObj),
            filter: aList.filter,
            loadnext: aList.loadnext
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            // console.log(response.data)
            aList.count = response.data.selectList.count
            aList.content = [...aList.content, ...response.data.selectList.content]
            aList.loadnext = response.data.selectList.loadnext
            aList.loaded = response.data.selectList.loadnext < 0
            aList.loading = false
            this.loading = false
            this.listContentLoadCheck()
          })
          .catch((err) => {
            console.log(err)
            aList.loading = false
            this.loading = false
          })
      }
    },
    listContentLoadCheck: _.debounce(function () {
      if (!this.loading && this.$refs.lcLoad) {
        this.$refs.lcLoad.some(function (aElement) {
          var bounding = aElement.getBoundingClientRect()
          if (bounding.top >= 0 && bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)) {
            this.getSelectListCont(aElement.dataset.listItem)
            return true
          }
        }, this)
      }
    }, 100)
  },
  computed: {
    sortFieldName () {
      return this.tabledata.data.options.ordering[0] || this.tabledata.data.model.ordering[0]
    },
    sortField () {
      return AllgemeineFunktionen.getFirstObjectOfValueInPropertyOfArray(this.tabledata.data.model.fields, 'field_name', this.sortFieldName)
    }
  },
  components: {
    DBFormSelectSearch,
    DBFormSelectFilter
  }
}
</script>

<style scoped>
.dbformsel-main {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.sel-l {
  padding-bottom: 4px;
}
button.btn-l, button.btn-cl {
  display: block;
  width: 100%;
  font-size: 16px;
  text-align: left;
  padding: 3px 10px;
  margin-bottom: 1px;
  background: #eee;
}
.sel-l.active button.btn-l {
  background: #ccc;
}
button.btn-l:hover, button.btn-l:focus {
  background: #ddd;
}
.sel-l.active button.btn-l:hover, .sel-l.active button.btn-l:focus {
  background: #bbb;
}
button.btn-l > i {
  font-style: normal;
  float: right;
}
.sel-l-loading {
  float: right;
  top: 4px;
}
.sel-c.active button.btn-cl {
  background: #666;
  color: #eee;
}
.sel-c-icon {
  float: right;
  color: #eee;
}
</style>
