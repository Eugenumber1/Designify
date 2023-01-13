<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <!-- bootswatch cdn -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/materia/bootstrap.min.css" integrity="sha384-B4morbeopVCSpzeC1c4nyV0d0cqvlSAfyXVfrPJa25im5p+yEN/YmhlgQP/OyMZD" crossorigin="anonymous">

      <div class="row">
        <h1 class="text-center bg-primary text-white">
          Describe your Brand
        </h1>
        <div class="col-lg-10">
          <hr><br>
          <!-- Alert message -->
          <button type="button" class="btn btn-success btn-sm" v-b-modal.word-modal>
            Tell us the Concept!</button>
          <br><br>
          <div  v-for="(photo, index) in photos" :key="index">
            <h2>The Word with which you associate your brand is: {{ photo.word }}</h2>
          <table class="table table-hover">
            <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Concept</th>
              <th scope="col">Photo</th>
              <th scope="col">Weight</th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="pic in photo.url" :key="pic">
                <td>{{ photo.id }}</td>
                <td>{{ photo.word }}</td>
                <td>
                  <img :src="pic" alt="photo" width="600" height="600">
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-info btn-sm">Add</button>
                    <button type="button" class="btn btn-danger btn-sm">Reduce</button>
                  </div>
                </td>
            </tr>
            </tbody>
          </table>
          </div>
          <div v-for="(photo, index) in photos" :key="index">
            <img v-bind:src="`${photo.url}`" alt="photo" width="100" height="100">
          </div>
        </div>
      </div>
      <!-- Modal -->
      <b-modal ref="addWordModal"
                   id="word-modal"
                   title="Add a new word"
                   hide-footer>
      <b-form @submit="onSubmit" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addWordForm.word"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">
            Submit
          </b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BModal } from 'bootstrap-vue';

export default {
  data() {
    return {
      photos: [],
      addWordForm: {
        word: '',
      },
    };
  },
  components: {
    BModal,
  },
  methods: {
    // get function
    getPhotos() {
      const path = 'http://localhost:5000/photos';
      axios.get(path)
        .then((res) => {
          this.photos = res.data.photos;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // post function
    postWord(payLoad) {
      const path = 'http://localhost:5000/photos';
      axios.post(path, payLoad)
        .then(() => {
          this.getPhotos();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    initForm() {
      this.addWordForm.word = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$bvModal.hide('word-modal');
      const payLoad = {
        word: this.addWordForm.word,
      };
      this.postWord(payLoad);
      this.initForm();
    },
  },
  created() {
    this.getPhotos();
  },
};
</script>
