const PostListMixin = {
  methods: {
    scroll_yielder() {
      if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight-100) {
        if (this.current_page < this.total_pages) {
          this.current_page = ++this.current_page;
          let vm = this;
          axios.get(vm.request_url)
          .then((r) => { vm.posts = vm.posts.concat(r.data.results); })
          .catch((err) => { console.log(err); });
        }
      }
    },
  },
  mounted() {
    this.$nextTick(() => {
      document.addEventListener('scroll', this.scroll_yielder);
    });
  },
  destroyed() {
    document.removeEventListener('scroll', this.scroll_yielder);
  },
}

let searchbox = new Vue({
  el: '#searchbox',
  data: {
    open_link: 1,
    search_line: 0,
  },
  methods: {
    OpenSearch() {
      this.open_link = 0;
      this.search_line = 1;

      setTimeout(()=>{ this.$el.querySelector('[type="text"]').focus()}, 100);
    },
    CloseSearch() {
      this.open_link = 1;
      this.search_line = 0;
    },
    sendform() {
        if (this.$el.querySelector('[type="text"]').value) {
          this.$el.querySelector('form').submit();
        } else {
          this.$el.querySelector('[type="text"]').focus();
        }
    }
  }
});