import Vue from 'vue';
import Router from 'vue-router';
import Photos from '../components/Photos.vue';
import Books from '../components/Books.vue';
import Ping from '../components/Ping.vue';
import ClientView from '../components/ClientView.vue';
import DesignerView from '../components/DesignerView.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Books',
      component: Books,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/photos',
      name: 'Photos',
      component: Photos,
    },
    {
      path: '/client',
      name: 'Client',
      component: ClientView,
    },
    {
      path: '/designer',
      name: 'Designer',
      component: DesignerView,
    },
  ],
});
