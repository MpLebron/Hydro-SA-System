import Vue from 'vue'
import Router from 'vue-router'
import ModelList from '@/views/modelList/ModelList'
import ModelContribute from '@/views/modelList/ModelContribute'
import SAPage from '@/views/saPage/SAPage'
import LibraryPage from '@/views/libraryPage/LibraryPage'
import LibraryContributePage from '@/views/libraryPage/LibraryContributePage'
import ProjectManagePage from '@/views/managePage/ProjectManagePage'
import ConvergencePage from '@/views/managePage/ConvergencePage'
import CredibilityPage from '@/views/managePage/CredibilityPage'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'ModelList',
      component: ModelList
    },
    {
      path: '/ModelContribute',
      name: 'ModelContribute',
      component: ModelContribute
    },
    {
      path: '/SAPage',
      name: 'SAPage',
      component: SAPage
    },
    {
      path: '/LibraryPage',
      name: 'LibraryPage',
      component: LibraryPage
    },
    {
      path: '/LibraryPage/LibraryContributePage',
      name: 'LibraryContributePage',
      component: LibraryContributePage
    },
    {
      path: '/ProjectManagePage',
      name: 'ProjectManagePage',
      component: ProjectManagePage
    },
    {
      path: '/ProjectManagePage/ConvergencePage',
      name: 'ConvergencePage',
      component: ConvergencePage
    },
    {
      path: '/ProjectManagePage/CredibilityPage',
      name: 'CredibilityPage',
      component: CredibilityPage
    }
  ]
})
