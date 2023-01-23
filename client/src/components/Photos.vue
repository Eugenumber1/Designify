<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <!-- bootswatch cdn -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css" integrity="sha384-B4morbeopVCSpzeC1c4nyV0d0cqvlSAfyXVfrPJa25im5p+yEN/YmhlgQP/OyMZD" crossorigin="anonymous">
      <div class="row">
        <h1 class="text-center bg-primary text-white">
          Describe your Brand
        </h1>
        <div class="col-lg-10">
          <hr><br>
          <!-- Alert message -->
          <b-alert variant="success" v-if="showMessage" show> {{ message }} </b-alert>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.word-modal>
            Tell us the Concept!</button>
          <br><br>
          <div  v-for="(photo_object, index_object) in photos" :key="index_object">
            <h2>The Word with which you associate your brand is: {{ photo_object.word }}</h2>
            <p> Change the weights of the photos or
              delete those which don't visually fit into your concept </p>
            <h3>When you are ready, and all
              photos ideally describe your brand - submit them to our AI</h3>
            <button type="button" class="btn btn-primary"
                    @click="sendConcept(photo_object.id)">
            Submit Concept</button>
            <button type="button" class="btn btn-danger"
                    @click="resetConcept(photo_object.id)">
            Reset Concept</button>
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
              <tr v-for="(photo, index_photo) in photo_object.url" :key="index_photo">
                <td>{{ index_photo }}</td>
                <td>{{ photo_object.word }}</td>
                <td>
                  <div v-if="photo[1]===1">
                    <img :src="photo[0]" alt="photo" width="100" height="100"></div>
                  <div v-else-if="photo[1]===2">
                    <img :src="photo[0]" alt="photo" width="200" height="200"></div>
                  <div v-else-if="photo[1]===3">
                    <img :src="photo[0]" alt="photo" width="300" height="300"></div>
                  <div v-else-if="photo[1]===4">
                    <img :src="photo[0]" alt="photo" width="400" height="400"></div>
                  <div v-else-if="photo[1]===5">
                    <img :src="photo[0]" alt="photo" width="500" height="500"></div>
                    <p>{{ photo[1] }}</p>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-info btn-sm" v-b-modal.weight-modal
                    @click="editWeight(photo_object.id, index_photo)">Edit Weight</button>
                    <button type="button" class="btn btn-danger btn-sm"
                            @click="deletePhoto(photo_object.id, index_photo)">Delete</button>
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
      <!-- Modal 2 -->
      <b-modal ref="editWeightModal"
                   id="weight-modal"
                   title="Update the Weight"
                   hide-footer hide-backdrop>
      <b-form @submit="onSubmitUpdate" class="w-100">
      <b-form-group id="form-weight-edit-group"
                    label="Title:"
                    label-for="form-weight-edit-input">
          <b-form-input id="form-weight-input"
                        type="text"
                        v-model="editForm.weight"
                        required
                        placeholder="Enter the Weight from 1 to 5">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">
            Submit
          </b-button>
        </b-button-group>
      </b-form>
    </b-modal>
      <!-- Modal 2 end -->
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
      editForm: {
        photo_object_id: '',
        photo_id: '',
        weight: 0,
      },
      // submitConceptForm: {
      //   photo_object_id: '',
      // },
    };
  },
  message: '',
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
          this.message = 'You are looking for a new word!';
          this.showMessage = true;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    initForm() {
      this.addWordForm.word = '';
      this.editForm.photo_object_id = '';
      this.editForm.photo_id = '';
      this.editForm.weight = 0;
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
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$bvModal.hide('weight-modal');
      const payLoad = {
        weight: this.editForm.weight,
      };
      this.updatePhoto(payLoad, this.editForm.photo_object_id, this.editForm.photo_id);
    },
    updatePhoto(payLoad, photoObjectId, photoId) {
      const path = `http://localhost:5000/photos/${photoObjectId}/${photoId}`;
      axios.put(path, payLoad)
        .then(() => {
          this.getPhotos();
          this.message = 'Photo Weight Updated!';
          this.showMessage = true;
        })
        .catch((err) => {
          console.error(err);
          this.getPhotos();
        });
    },
    sendConcept(photoObjectId) {
      const path = `http://localhost:5000/concept/${photoObjectId}`;
      axios.post(path)
        .then(() => {
          this.getPhotos();
          this.message = 'You just submitted your concept!';
          this.showMessage = true;
        })
        .catch((err) => {
          console.error(err);
          this.getPhotos();
        });
    },
    // Handle update button
    editWeight(photoObjectId, photoIndex) {
      this.editForm.photo_object_id = photoObjectId;
      this.editForm.photo_id = photoIndex;
    },
    // handle removal of the photos which don't fit
    removePhoto(photoObjectId, photoId) {
      const path = `http://localhost:5000/photos/${photoObjectId}/${photoId}`;
      axios.delete(path)
        .then(() => {
          this.getPhotos();
          this.message = 'Photo removed';
          this.showMessage = true;
        })
        .catch((err) => {
          console.error(err);
          this.getPhotos();
        });
    },
    resetConcept(photoObjectId) {
      const path = `http://localhost:5000/concept/${photoObjectId}`;
      axios.delete(path)
        .then(() => {
          this.getPhotos();
          this.message = 'You just reset your concept, now you can try creating a new one!';
          this.showMessage = true;
        })
        .catch((err) => {
          console.error(err);
          this.getPhotos();
        });
    },
    // Handle delete button
    deletePhoto(photoObjectId, photoId) {
      this.removePhoto(photoObjectId, photoId);
    },
  },
  created() {
    this.getPhotos();
  },
};
</script>
