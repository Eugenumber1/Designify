<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <!-- bootswatch cdn -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css" integrity="sha384-B4morbeopVCSpzeC1c4nyV0d0cqvlSAfyXVfrPJa25im5p+yEN/YmhlgQP/OyMZD" crossorigin="anonymous">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" integrity="sha512-+4zCK9k+qNFUR5X+cKL9EIR+ZOhtIloNl9GIKS57V1MyNsYpYcUrUeQc9vNfzsWfV28IaLL3i96P9sdNyeRssA==" crossorigin="anonymous" />
      <div class="row">
        <h1 class="text-center text-uppercase text-black">
          Describe your Brand
        </h1>
        <div class="col-sm-12">
          <hr><br>
          <!-- Alert message -->
          <b-alert variant="success" v-if="showMessage" show> {{ message }} </b-alert>
          <div class="text-md-left">
          <h2>Process</h2>
              <p>Tell us with which values you truly identify your brand with and our AI will create
                several mood boards to help the designer better understand your brand.</p>
            </div>
          <button type="button" class="btn btn-primary btn-sm " v-b-modal.word-modal>
            Tell us the Concept!</button>
          <br><br>
          <div  v-for="(photo_object, index_object) in photosPositive" :key="index_object">
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
          <div v-for="(photoObject, index) in photosPositive" :key="index">
            <div v-for="([source, weight], indexPhoto) in photoObject.url"
                 :key="indexPhoto"
            class="grid-container">
              <div @mouseenter="isHovered = true; indexHovered=indexPhoto"
                    @mouseleave="isHovered = false; indexHovered=null">
                <div class="picture" >
                    <img :src="source"
                         alt="photo"
                         class="img-thumbnail grid-container"
                         :style="imageStyles(weight, indexPhoto)">
                  <div v-if="activePhotoButtons === indexPhoto && isHovered===true">
                  <div class="left-side"
                       @click="increaseWeight(photo_object.id, indexPhoto, weight)"></div>
                  <div class="right-side"
                       @click="decreaseWeight(photo_object.id, indexPhoto, weight)"></div>
                    <div class="delete-button">
                      <button @click="deletePhoto(photo_object.id, indexPhoto)" type="button"
                              class="btn btn-danger btn-sm float-right">
                              <i class="fas fa-times"></i>
                      </button>
                    </div>
                    </div>
                <!--<div v-if="activePhotoButtons === indexPhoto && isHovered===true"
                     class="btn-group" role="group">
                    <button type="button" class="btn btn-info btn-sm btn-left"
                            v-b-modal.weight-modal
                    @click="editWeight(photo_object.id, indexPhoto)">Edit Weight</button>
                    <button type="button" class="btn btn-danger btn-sm btn-right"
                            @click="deletePhoto(photo_object.id, indexPhoto)">Delete</button>
                  </div>-->
                  </div>
                </div>
            </div>
            </div>
            <!--Here we have the photos with which the user doesn't associate his
            brand, mostly random ones -->
            <div v-for="(photoObject, index) in photosNegative" :key="index">
            <div v-for="([source, weight], indexPhoto) in photoObject.url"
                 :key="indexPhoto"
            class="grid-container">
              <div @mouseenter="isHovered = true; indexHovered=indexPhoto"
                    @mouseleave="isHovered = false; indexHovered=null">
                <div class="picture" >
                    <img :src="source"
                         alt="photo"
                         class="img-thumbnail grid-container"
                         :style="imageStyles(weight, indexPhoto)">
                  <div v-if="activePhotoButtons === indexPhoto && isHovered===true">
                  <div class="left-side"
                       @click="increaseWeight(photo_object.id, indexPhoto, weight)"></div>
                  <div class="right-side"
                       @click="decreaseWeight(photo_object.id, indexPhoto, weight)"></div>
                    <div class="delete-button">
                      <button @click="deletePhoto(photo_object.id, indexPhoto)" type="button"
                              class="btn btn-danger btn-sm float-right">
                              <i class="fas fa-times"></i>
                      </button>
                    </div>
                    </div>
                  </div>
                </div>
            </div>
            </div>
            <!--
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
          -->
          </div>
        </div>
        <div>
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
      isHovered: false,
      indexHovered: '',
      photosPositive: [],
      photosNegative: [],
      addWordForm: {
        word: '',
      },
      editForm: {
        photo_object_id: '',
        photo_id: '',
        weight: 0,
      },
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
          this.photosPositive = res.data.photosPositive;
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
    // Handle update button
    editWeight(photoObjectId, photoIndex) {
      this.editForm.photo_object_id = photoObjectId;
      this.editForm.photo_id = photoIndex;
    },
    decreaseWeight(photoObjectId, indexPhoto, weight) {
      const payload = {
        weight: weight - 1,
      };
      this.updatePhoto(payload, photoObjectId, indexPhoto);
    },
    increaseWeight(photoObjectId, indexPhoto, weight) {
      const payload = {
        weight: weight + 1,
      };
      this.updatePhoto(payload, photoObjectId, indexPhoto);
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
    // Handle delete button
    deletePhoto(photoObjectId, photoId) {
      this.removePhoto(photoObjectId, photoId);
    },
    // making styles for each photo
    // imageStyles(weight, index_photo) {
    //   return {
    //     width: `${weight * 100}px`,
    //     height: `${weight * 100}px`,
    //     borderRadius: '1px',
    //     ...(this.isHovered ? {
    //       transform: 'scale(1.05)',
    //       boxShadow: '5px 5px 10px #ccc',
    //     } : {}),
    //   };
    // },
    // imageStyles(weight, indexPhoto) {
    //   // this.$refs[`img-${indexPhoto}`].style.width = `${weight * 10}px`;
    //   // this.$refs[`img-${indexPhoto}`].style.height = `${weight * 10}px`;
    //   //console.log(indexPhoto);
    //   //this.changeOnHover(indexPhoto);
    //   return {
    //     width: `${weight * 100}px`,
    //     height: `${weight * 100}px`,
    //     borderRadius: '1px',
    //     ...if (this.isHovered && this.indexHovered === indexPhoto){
    //       transform = 'scale(1.05)';
    //       boxShadow = '5px 5px 10px #ccc';
    //   }
    //   };
    // },
    imageStyles(weight, indexPhoto) {
      const styles = {
        width: `${weight * 25 + 200}px`,
        height: `${weight * 25 + 200}px`,
        borderRadius: '1px',
      };
      if (this.isHovered && this.indexHovered === indexPhoto) {
        styles.transform = 'scale(1.05)';
        styles.boxShadow = '5px 5px 10px #ccc';
        styles.transition = 'all .5s ease';
        // styles.vertical-align = 'middle';
      }
      return styles;
    },
    // changeOnHover(indexPhoto) {
    //   if (this.isHovered && this.indexHovered === indexPhoto) {
    //     this.$refs[`img-${indexPhoto}`].style.transform = 'scale(1.05)';
    //     this.$refs[`img-${indexPhoto}`].style.boxShadow = '5px 5px 10px #ccc';
    //   }
    // },
  },
  computed: {
    activePhotoButtons() {
      return this.indexHovered;
    },
  },
  created() {
    this.getPhotos();
  },
};
</script>
<style>
.picture {
    position: relative;
  }

  .btn-group {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .btn-left {
    position:absolute;
    left:0;
  }

  .btn-right {
    position:absolute;
    right:0;
  }
.picture {
  margin: 5px;
}
.image-cloud {
  justify-content: center;
}
.grid-container {
  display: inline-grid;
  column-gap: 5px;
  row-gap: 5px;
  grid-template-columns: auto auto auto auto auto;
  grid-template-rows: auto auto auto;
}
.left-button {
    position: absolute;
    left: 0;
}

.right-button {
    position: absolute;
    right: 0;
}
.picture {
    position: relative;
}
.btn-group {
    position: absolute;
    bottom: 0;
    left: 0;
}
.left-side, .right-side {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 50%;
  transition: 0.3s ease-in-out;
}

.left-side {
  left: 0;
}

.right-side {
  right: 0;
}
.delete-button {
  position: absolute;
  top: 0;
  right: 0;
}
</style>
