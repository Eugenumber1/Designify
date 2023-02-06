<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <!-- bootswatch cdn -->
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css" integrity="sha384-B4morbeopVCSpzeC1c4nyV0d0cqvlSAfyXVfrPJa25im5p+yEN/YmhlgQP/OyMZD" crossorigin="anonymous">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" integrity="sha512-+4zCK9k+qNFUR5X+cKL9EIR+ZOhtIloNl9GIKS57V1MyNsYpYcUrUeQc9vNfzsWfV28IaLL3i96P9sdNyeRssA==" crossorigin="anonymous" />
      <div class="row">

        <div class="col-sm-12">
          <hr><br>
          <!-- Alert message -->
          <div class="text-md-left">
            <h1>Moodboard Photos</h1>
            <div class="moodboards">
              <div  v-for="(moodboard, index_object) in moodboards" :key="index_object">
          <div v-for="(moodboard, index) in moodboards" :key="index">
            <div class="photo-clusters">
            <div v-for="(source, indexPhoto) in moodboard.urls"
                 :key="indexPhoto"
            class="grid-container">
              <div @mouseenter="isHovered = true; indexHovered=indexPhoto"
                    @mouseleave="isHovered = false; indexHovered=null">
                <div class="picture" >
                    <img :src="source"
                         alt="photo"
                         class="img-thumbnail grid-container"
                         :style="imageStyles(indexPhoto)">
                    <div class="delete-button">
                      <button @click="deletePhoto(moodboard.id, indexPhoto)" type="button"
                              class="btn btn-danger btn-sm float-right">
                              <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                </div>
            </div>
            </div>
            </div>
          <br><br>
        </div>
        <div>
          </div>
      </div>
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
      isHovered: false,
      indexHovered: '',
      moodboards: [],
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
  methods: {
    // get function
    getMoodboards() {
      const path = 'http://localhost:5000/designer/moodboard';
      axios.get(path)
        .then((res) => {
          this.moodboards = res.data.moodboards;
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
    imageStyles(indexPhoto) {
      const styles = {
        width: `${300}px`,
        height: `${300}px`,
        borderRadius: '1px',
      };
      if (this.isHovered && this.indexHovered === indexPhoto) {
        styles.transform = 'scale(1.05)';
        styles.boxShadow = '5px 5px 10px #ccc';
        styles.transition = 'all .5s ease';
      }
      return styles;
    },
  },
  computed: {
    activePhotoButtons() {
      return this.indexHovered;
    },
  },
  created() {
    this.getMoodboards();
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
.photo-clusters {
  display: inline;
}
</style>
