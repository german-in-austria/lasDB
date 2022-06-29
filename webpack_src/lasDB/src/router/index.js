import Vue from 'vue'
import Router from 'vue-router'
import MainPage from '@/sites/MainPage'
import EditData from '@/sites/EditData'
import EditInformants from '@/sites/EditInformants'
import EditLocations from '@/sites/EditLocations'
import EditQuestions from '@/sites/EditQuestions'
import EditVariables from '@/sites/EditVariables'
import EditVariantgroups from '@/sites/EditVariantgroups'
import EditLanguages from '@/sites/EditLanguages'
import EditVariantgroupTypes from '@/sites/EditVariantgroupTypes'
import AssignmentVariantgroups from '@/sites/AssignmentVariantgroups'
import MapVariantgroups from '@/sites/MapVariantgroups'
import ToolsHcbDiagram from '@/sites/ToolsHcbDiagram'
import ToolsDBForm from '@/sites/ToolsDBForm'
import ToolsMap from '@/sites/ToolsMap'
import ResultsMap from '@/sites/ResultsMap'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MainPage',
      component: MainPage
    },
    {
      path: '/edit/data/',
      name: 'EditData',
      component: EditData
    },
    {
      path: '/edit/informants/',
      name: 'EditInformants',
      component: EditInformants
    },
    {
      path: '/edit/locations/',
      name: 'EditLocations',
      component: EditLocations
    },
    {
      path: '/edit/questions/',
      name: 'EditQuestions',
      component: EditQuestions
    },
    {
      path: '/edit/variables/',
      name: 'EditVariables',
      component: EditVariables
    },
    {
      path: '/edit/assignmentvariantgroups/',
      name: 'AssignmentVariantgroups',
      component: AssignmentVariantgroups
    },
    {
      path: '/edit/variantgroups/',
      name: 'EditVariantgroups',
      component: EditVariantgroups
    },
    {
      path: '/edit/languages/',
      name: 'EditLanguages',
      component: EditLanguages
    },
    {
      path: '/edit/variantgrouptypes/',
      name: 'EditVariantgroupTypes',
      component: EditVariantgroupTypes
    },
    {
      path: '/edit/mapvariantgroups/',
      name: 'MapVariantgroups',
      component: MapVariantgroups
    },
    {
      path: '/results/map/',
      name: 'ResultsMap',
      component: ResultsMap,
      props: route => ({ query: route.query })
    },
    {
      path: '/results/explore/',
      name: 'ResultsExplore',
      component: ResultsMap,
      props: route => ({ query: route.query })
    },
    {
      path: '/tools/map/',
      name: 'ToolsMap',
      component: ToolsMap
    },
    {
      path: '/tools/diagram/',
      name: 'ToolsHcbDiagram',
      component: ToolsHcbDiagram
    },
    {
      path: '/tools/dbform/',
      name: 'ToolsDBForm',
      component: ToolsDBForm
    }

  ]
})
