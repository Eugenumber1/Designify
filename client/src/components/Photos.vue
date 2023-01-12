<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <!-- bootswatch cdn -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/materia/bootstrap.min.css" integrity="sha384-B4morbeopVCSpzeC1c4nyV0d0cqvlSAfyXVfrPJa25im5p+yEN/YmhlgQP/OyMZD" crossorigin="anonymous">

      <div class="row">
        <h1>Describe your Brand</h1>
        <div class="col-lg-10">
          <hr><br>
          <!-- Alert message -->
          <input v-model.trim="word" type="text" id="word-concept"/>
          <button type="button" class="btn btn-success btn-sm">Tell us the Concept!</button>
          <br><br>
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
              <tr v-for="(photo, index) in photos" :key="index">
                <td>{{ photo.id }}</td>
                <td>{{ photo.word }}</td>
                <td>
                  <img :src="photo.url[0]" alt="photo" width="100" height="100">
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

          <div v-for="(photo, index) in photos" :key="index">
            <img v-bind:src="`${photo.url}`" alt="photo" width="100" height="100">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      photos: [],
    };
  },
  methods: {
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
  },
  created() {
    this.getPhotos();
  },
};
</script>
