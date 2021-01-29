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
        @change="updateFirebase(abstract.id, abstract.included)"
        buttons
      ></b-form-radio-group>
    </b-form-group> 

    </b-card>
      </div>
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
      abstracts: [],
      includeOptions: [
          { text: 'Include', value: 'included' },
          { text: 'Exclude', value: 'excluded' },
          { text: 'reset', value: 'new'}
        ],
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
    updateFirebase(id, state) {
        db.ref("review_results/"+id).update({included: state});
    },
    getAbstracts() {
      var abstractData = [];
      absRef.once('value', (snapshot) => {
        snapshot.forEach((doc) => {
          /* console.log(doc.getRef()); */
          console.log(doc);
          abstractData.push({id: doc.ref_.path.pieces_[1],
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
  },
  created() {
    this.getAbstracts();
  }
};
</script>
