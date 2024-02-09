<template>
  <div class="container">
    <div class="row">
      <div class="col-md-8">
        <!-- <h1>Constituencies</h1> -->
        <div v-for="item in data" :key="item.id">
          <h2>{{ item.name }}</h2>
          <p v-for="winner in item.winning" :key="winner.id">
            <b>Winner:</b> {{ winner }}
          </p>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Party</th>
                <th scope="col">Vote Count</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="party_vote_count in item.vote_counts">
                <td scope="row">{{ party_vote_count.party }}</td>
                <td>{{ party_vote_count.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      data: ['']
    }
  },
  methods: {
    async getData() {
      try {
        // fetch tasks
        const response = await axios.get('/api/constituencies/');
        // set the data returned as tasks
        this.data = response.data; 
      } catch (error) {
        // log the error
        console.log(error);
      }
    },
  },
  created() {
    // Fetch tasks on page load
    this.getData();
  }
}
</script>
