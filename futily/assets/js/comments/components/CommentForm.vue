<template>
  <form class="frm-Form cmm-Form" @submit.prevent="handleSubmit">
    <div class="frm-Form_Items frm-Form_Items-tight">
      <div class="frm-Form_Item">
        <div class="cmm-Form_Preview" v-html="preview" v-show="message.length > 0"></div>

        <label class="frm-Form_Label" for="message">Message</label>

        <textarea class="frm-Form_Textarea"
                  name="message"
                  id="message"
                  v-model="message"></textarea>
      </div>
    </div>

    <div class="frm-Form_Actions">
      <button type="submit" class="frm-Form_Submit btn-Primary cmm-Form_Submit">Submit</button>
      <button class="frm-Form_Submit btn-Secondary cmm-Form_Cancel"
              type="reset"
              @click="$emit('CommentForm:cancelled')">Cancel
      </button>
    </div>
  </form>
</template>

<script>
  import Remarkable from 'remarkable';
  import { mapActions, mapGetters } from 'vuex';

  import * as types from '../types';
  import { debounce } from '../../utils';

  export default {
    props: {
      replyTo: Number,
    },

    data () {
      return {
        followUp: false,
        message: '',
        md: new Remarkable({
          components: {
            core: {
              rules: [
                'block',
                'inline',
                'references',
                'replacements',
                'linkify',
                'smartquotes',
                'references',
              ],
            },
            block: {
              rules: [
                'blockquote',
                'code',
                'hr',
                'list',
                'paragraph',
                'table',
              ],
            },
            inline: {
              rules: [
                'autolink',
                'backticks',
                'del',
                'emphasis',
                'escape',
                'links',
                'newline',
                'text',
              ],
            },
          },
        }),
      };
    },

    computed: {
      ...mapGetters({
        'config': types.GET_CONFIG,
      }),

      preview () {
        return this.md.render(this.message);
      },
    },

    methods: {
      ...mapActions({
        'loadComments': types.LOAD_COMMENTS,
      }),

      async handleSubmit (evt) {
        const form = this.config.form;

        const data = {
          content_type: form.contentType,
          object_pk: form.objectPk,
          timestamp: form.timestamp,
          security_hash: form.securityHash,
          honeypot: '',
          comment: this.preview,
          followup: this.followup,
          reply_to: this.replyTo || 0,
          email: '',
          name: '',
        };

        await this.$http({
          data,
          method: 'POST',
          url: this.config.sendUrl,
          xsrfCookieName: 'csrftoken',
          xsrfHeaderName: 'X-CSRFToken',
        });

        this.loadComments();
        this.message = '';

        this.$emit('CommentForm:saved');
      },

      handleContentInput: debounce(function (evt) {
        this.message = evt.target.value;
      }, 300),
    },
  };
</script>
