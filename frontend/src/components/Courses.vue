<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>RobotReviewer Live abstract screening</h1>
        <hr />
        <br /><br />
        <alert :message="message" v-if="showMessage"></alert>
        <br /><br />
    <span v-if="numberTodo>0">{{ numberTodo }} / {{ numberTotal }} still to screen</span>
    <span v-else>All done!</span>
    <div v-for="(abstract, index) in abstracts" :key="abstract.id">
    <b-card
        :title="abstract.ti"
        :header="abstract.citation"
        :header-text-variant="headerText(abstract.included)"
        :header-bg-variant="headerBack(abstract.included)"

        >
    <b-card-text>{{abstract.ab}}</b-card-text>
       <b-form-group
      v-slot="{ ariaDescribedby }"
    >
      <b-form-radio-group
        v-model="abstract.included"
        :options="includeOptions"
        :aria-describedby="ariaDescribedby"
        button-variant="outline-primary"
        size="lg"
        name="radio-btn-outline"
        buttons
      ></b-form-radio-group>
    </b-form-group> 

    </b-card>
    </div>
    <b-table striped hover :items="abstracts">
          <template #cell(included)="data">
            <input type="checkbox" v-model="data.included" />
       </template>
    </b-table>


        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Pubmed ID</th>
              <th scope="col">Citation</th>
              <th scope="col">Title</th>
              <th scope="col">To screen</th>
              <th scope="col">Included in review?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(abstract, index) in abstracts" :key="abstract.id">
              <td>{{ abstract.pmid}}</td>
              <td>{{ abstract.citation}}</td>
              <td>{{ abstract.ti}}</td>
              <td>
                <span v-if="abstract.to_screen">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
              <input type="checkbox" id="checkbox" v-model="abstract.included">
              <label for="checkbox"><span v-if="abstract.included"> yes</span><span v-else> no</span></label>
              <!--<td>${{ course.NValue }}</td>-->
              </td>
              <td>

                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn pill btn-info btn-sm"
                    v-b-modal.course-update-modal
                    @click="editCourse(course)"
                  >
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteCourse(course)"
                  >
                    Delete
                  </button>


                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <b-modal ref="addCourseModal" id="course-modal" title="Add a new Review" hide-footer>
          <b-form @submit="onSubmit" @reset="onReset" class="w-100">

          <b-form-group id="form-ReviewID-group" label="ReviewID:" label-for="form-ReviewID-input">
            <b-form-input
              id="form-ReviewID-input"
              type="text"
              v-model="addCourseForm.ReviewID"
              required
              placeholder="Enter ReviewID"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group id="form-PubmedID-group" label="PubmedID:" label-for="form-PubmedID-input">
            <b-form-input
              id="form-PubmedID-input"
              type="text"
              v-model="addCourseForm.PubmedID"
              required
              placeholder="Enter PubmedID"
            >
            </b-form-input>
          </b-form-group>

            <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
              <b-form-input
                id="form-title-input"
                type="text"
                v-model="addCourseForm.title"
                required
                placeholder="Enter title"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-abstract-group" label="Abstract:" label-for="form-abstract-input">
              <b-form-input
                id="form-abstract-input"
                type="text"
                v-model="addCourseForm.abstract"
                required
                placeholder="Enter Abstract"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-NValue-group" label="NValue:" label-for="form-NValue-input">
              <b-form-input
                id="form-NValue-input"
                type="number"
                step="0.01"
                v-model="addCourseForm.NValue"
                required
                placeholder="Enter NValue"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-ToBeScreened-group">
              <b-form-checkbox-group v-model="addCourseForm.ToBeScreened" id="form-checks">
                <b-form-checkbox value="true">ToBeScreened</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>

            <b-form-group id="form-Inclusion-group">
              <b-form-checkbox-group v-model="addCourseForm.Inclusion" id="form-checks">
                <b-form-checkbox value="true">Inclusion</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>

            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="cancel" variant="danger">Cancel</b-button>
          </b-form>
        </b-modal>
        <b-modal ref="editCourseModal" id="course-update-modal" title="Update" hide-footer>
          <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">

          <b-form-group
            id="form-PubmedID-edit-group"
            label="PubmedID:"
            label-for="form-PubmedID-edit-input"
          >
            <b-form-input
              id="form-PubmedID-edit-input"
              type="text"
              v-model="editForm.PubmedID"
              required
              placeholder="Enter PubmedID"
            >
            </b-form-input>
          </b-form-group>

            <b-form-group
              id="form-title-edit-group"
              label="Title:"
              label-for="form-title-edit-input"
            >
              <b-form-input
                id="form-title-edit-input"
                type="text"
                v-model="editForm.title"
                required
                placeholder="Enter title"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group
              id="form-abstract-edit-group"
              label="Abstract:"
              label-for="form-abstract-edit-input"
            >
              <b-form-input
                id="form-abstract-edit-input"
                type="text"
                v-model="editForm.abstract"

                placeholder="Enter Abstract"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-NValue-edit-group"
              label="Enter NValue:"
              label-for="form-NValue-edit-input"
            >
              <b-form-input
                id="form-NValue-edit-input"
                type="number"
                step="0.01"
                v-model="editForm.NValue"
                required
                placeholder="Enter NValue"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-ToBeScreened-edit-group">
              <b-form-checkbox-group v-model="editForm.ToBeScreened" id="form-checks">
                <b-form-checkbox value="true">To Be Screened?</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>

            <b-form-group id="form-Inclusion-edit-group">
              <b-form-checkbox-group v-model="editForm.Inclusion" id="form-checks">
                <b-form-checkbox value="true">To Be Included?</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>

            <b-button-group>
              <b-button type="submit" variant="primary">Update</b-button>
              <b-button type="reset" variant="danger">Cancel</b-button>
            </b-button-group>
          </b-form>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Alert from "./Alert.vue";
import firebase from "../firebaseInit";


const db = firebase.database()
const absRef = db.ref('review_results')

export default {
  data() {
    return {
      isProduction: false,
      email: "test@gmail.com",
      country: "UK",
      custom: {
        title: "rrlive test"
      },
      abstracts: [],
      includeOptions: [
          { text: 'Include', value: 'included' },
          { text: 'Exclude', value: 'excluded' },
        ],
      addCourseForm: {
        ReviewID: "",
        PubmedID: "",
        title: "",
        abstract: "",
        ToBeScreened: [],
        Inclusion: [],
        NValue: ""
      },
      editForm: {
        id: "",
        ReviewID: "",
        PubmedID: "",
        title: "",
        abstract: "",
        ToBeScreened: [],
        Inclusion: [],
        NValue: ""
      },
      message: "",
      showMessage: false
    };
  },
  components: {
    alert: Alert,

  },
  computed: {
    reference() {
      let text = "";
      let possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      for (let i = 0; i < 10; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
      return text;
    },
    numberTodo() {
        return this.abstracts.filter(abstract => (abstract.included=='new')).length;
    },
    numberTotal() {
        return this.abstracts.length;
    },
    filteredAbs() {
      return this.abstracts.filter(item => {
         return item.data.included
      })
    },
    orderedAbs() {
        return _.orderBy(this.abstracts, '')
  }
  },
  methods: {
    getAbstracts() {
      var abstractData = [];
      absRef.once('value', (snapshot) => {
        snapshot.forEach((doc) => {
          abstractData.push({id: doc.id,
                             pmid: doc.val().pmid,
                             ti: doc.val().ti,
                             ab: doc.val().ab,
                             citation: doc.val().citation,
                             included: doc.val().included,
                             to_screen: doc.val().to_screen}

            )
        })
        });
        this.abstracts = abstractData;
    },
    headerText(state) {
        if (state=='new') {return "white"} else {return "dark"}
    },
    headerBack(state) {
        if (state=='new') {return "info"} else {return "light"}
    },
    addCourse(payload) {
      const path = "http://localhost:5000/courses";
      axios
        .post(path, payload)
        .then(() => {
          this.getCourses();
          this.message = "Review Added!";
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getCourses();
        });
    },
    removeCourse(courseID) {
      const path = `http://localhost:5000/courses/${courseID}`;
      axios
        .delete(path)
        .then(() => {
          this.getCourses();
          this.message = "Review removed!";
          this.showMessage = true;
        })
        .catch(error => {
          console.error(error);
          this.getCourses();
        });
    },
    onDeleteCourse(course) {
      this.removeCourse(course.id);
    },
    initForm() {
      this.addCourseForm.ReviewID = "";
      this.addCourseForm.PubmedID = "";
      this.addCourseForm.title = "";
      this.addCourseForm.abstract = "";
      this.addCourseForm.ToBeScreened = [];
      this.addCourseForm.Inclusion = [];
      this.addCourseForm.NValue = "";
      this.editForm.id = "";
      this.editForm.ReviewID = "";
      this.editForm.PubmedID = "";
      this.editForm.title = "";
      this.editForm.abstract = "";
      this.editForm.ToBeScreened = [];
      this.editForm.Inclusion = [];
      this.editForm.NValue = "";
    },
    editCourse(course) {
      this.editForm = course;
    },
    onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editCourseModal.hide();
      let ToBeScreened = false;
      let Inclusion = false;
      if (this.editForm.ToBeScreened[0]) ToBeScreened = true;
      if (this.editForm.Inclusion[0]) Inclusion = true;
      const payload = {
        ReviewID: this.editForm.ReviewID,
        PubmedID: this.editForm.PubmedID,
        title: this.editForm.title,
        abstract: this.editForm.abstract,
        ToBeScreened,
        Inclusion,
        NValue: this.editForm.NValue
      };
      this.updateCourse(payload, this.editForm.id);
    },
    updateCourse(payload, courseID) {
      const path = `http://localhost:5000/courses/${courseID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getCourses();
          this.message = "Review updated!";
          this.showMessage = true;
        })
        .catch(error => {
          console.error(error);
          this.getCourses();
        });
    },
    onSubmit(e) {
      e.preventDefault();
      this.$refs.addCourseModal.hide();
      let ToBeScreened = false;
      let Inclusion = false;
      if (this.addCourseForm.ToBeScreened[0]) ToBeScreened = true;
      if (this.addCourseForm.Inclusion[0]) Inclusion = true;
      const payload = {
        ReviewID: this.addCourseForm.ReviewID,
        PubmedID: this.addCourseForm.PubmedID,
        title: this.addCourseForm.title,
        abstract: this.addCourseForm.abstract,
        ToBeScreened,
        Inclusion,
        NValue: this.addCourseForm.NValue
      };
      this.addCourse(payload);
      this.initForm();
    },
    onReset(e) {
      e.preventDefault();
      this.$refs.addCourseModal.hide();
      this.initForm();
    },
    onResetUpdate(e) {
      e.preventDefault();
      this.$refs.editCourseModal.hide();
      this.initForm();
      this.getCourses();
    }
  },
  created() {
    this.getAbstracts();
  }
};
</script>
