<template>
  <article :class="['cmm-Comment', {'cmm-Comment-active': showForm || showReportForm }]">
    <header class="cmm-Comment_Header">
      <a class="cmm-Comment_User" :href="data.user_url">
        <img class="cmm-Comment_UserImage" :src="data.user_avatar" v-if="data.user_avatar">
        <span class="cmm-Comment_UserName">{{ data.user_name }}</span>
      </a>

      <time class="cmm-Comment_Time">{{ data.submit_date }}</time>
    </header>

    <div class="cmm-Comment_Controls">
      <button class="cmm-Comment_Upvote"
              :aria-selected="currentVote === 'like'"
              @click.prevent="sendFeedback('like')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 404.257 404.257">
          <path d="M386.257 114.33l-184.13 138.097L18 114.33l-18 24 202.128 151.597 202.13-151.596" />
        </svg>
      </button>

      <span :class="['cmm-Comment_Score', scoreClass]">{{ score }}</span>

      <button class="cmm-Comment_Downvote"
              :aria-selected="currentVote === 'dislike'"
              @click.prevent="sendFeedback('dislike')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 404.257 404.257">
          <path d="M386.257 114.33l-184.13 138.097L18 114.33l-18 24 202.128 151.597 202.13-151.596" />
        </svg>
      </button>
    </div>

    <div class="cmm-Comment_Content md-Markdown" v-html="data.comment"></div>

    <footer class="cmm-Comment_Footer" v-if="config.isAuthenticated">
      <button class="cmm-Comment_Reply" @click="activateReplyForm">Reply</button>
      <button :class="['cmm-Comment_Report', {'cmm-Comment_Report-active': showReportForm}]"
              @click="activateReportForm">Report
      </button>

      <form class="cmm-Comment_ReportForm frm-Form"
            v-if="showReportForm"
            @submit.prevent="submitReportForm">
        <CsrfToken />
        <div class="frm-Form_Items frm-Form_Items-tight">
          <div class="frm-Form_Item">
            <label class="frm-Form_Label" for="comment">Message</label>

            <textarea class="frm-Form_Textarea"
                      name="comment"
                      id="comment"
                      ref="reportFormComment"
                      v-model="reportComment"></textarea>

            <div class="frm-Form_Extra">
              <p class="frm-Form_Help">Please leave a message if required.<br><strong>Remember abuse of this system can get you in trouble.</strong>
              </p>
            </div>
          </div>
        </div>

        <div class="frm-Form_Actions">
          <button type="submit" class="frm-Form_Submit btn-Primary">Send</button>
        </div>
      </form>

      <p class="cmm-Comment_Reported"
         v-if="reported">Thank you for reporting this comment, we will take a look at it shortly.</p>

      <div class="cmm-Comment_Form" v-if="showForm">
        <CommentForm :replyTo="data.id"
                     @CommentForm:saved="showForm = false"
                     @CommentForm:cancelled="showForm = false" />
      </div>
    </footer>
  </article>
</template>

<script>
  import { mapGetters } from 'vuex';

  import CommentForm from './CommentForm.vue';
  import CsrfToken from '../../vue/components/CsrfToken.vue';
  import * as types from '../types';

  export default {
    components: {
      CommentForm,
      CsrfToken,
    },

    props: {
      data: Object,
    },

    created () {
      this.likes = this.data.flags.like.users.length;
      this.dislikes = this.data.flags.dislike.users.length;
      this.currentVote = this.data.flags.like.users.includes(this.config.currentUser)
        ? 'like'
        : this.data.flags.dislike.users.includes(this.config.currentUser)
          ? 'dislike'
          : '';
    },

    data () {
      return {
        reportComment: '',
        showReportForm: false,
        showForm: false,
        reported: false,
        likes: 0,
        dislikes: 0,
        currentVote: '',
      };
    },

    computed: {
      ...mapGetters({
        'config': types.GET_CONFIG,
      }),

      score () {
        return this.likes - this.dislikes;
      },

      scoreClass () {
        return this.score > 0
          ? 'cmm-Comment_Score-positive'
          : this.score < 0
            ? 'cmm-Comment_Score-negative'
            : '';
      },
    },

    methods: {
      activateReplyForm () {
        this.showForm = true;
        this.showReportForm = false;

        this.$nextTick(() => this.$el.querySelector('.cmm-Comment_Form textarea').focus());
      },

      activateReportForm () {
        this.showForm = false;
        this.showReportForm = true;

        this.$nextTick(() => this.$refs.reportFormComment.focus());
      },

      async sendFeedback (flag) {
        if (this.config.isAuthenticated && flag !== this.currentVote) {
          try {
            await this.$http({
              method: 'POST',
              url: this.config.feedbackUrl,
              data: {
                flag,
                comment: this.data.id,
              },
              xsrfCookieName: 'csrftoken',
              xsrfHeaderName: 'X-CSRFToken',
            });

            if (this.currentVote === 'dislike' && flag === 'like') {
              this.likes += 1;
              this.dislikes -= 1;
            } else if (this.currentVote === 'like' && flag === 'dislike') {
              this.likes -= 1;
              this.dislikes += 1;
            } else {
              this.likes += flag === 'like' ? 1 : 0;
              this.dislikes += flag === 'dislike' ? 1 : 0;
            }

            this.currentVote = flag;
          } catch (e) {
            console.error(e);
          }
        }
      },

      async submitReportForm () {
        try {
          const res = await this.$http({
            method: 'POST',
            url: this.config.flagUrl,
            data: {
              comment: this.data.id,
              flag: 'report',
            },
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
          });

          if (res.status === 201) {
            this.showReportForm = false;
            this.reported = true;
          }
        } catch (e) {
          console.error(e);
        }
      },
    },
  };
</script>
