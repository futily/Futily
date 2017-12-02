export default {
  functional: true,

  props: {
    class: String,
    isLink: Boolean,
  },

  render (h, context) {
    return h(
      context.props.isLink ? 'a' : 'div',
      context.data,
      context.children
    );
  },
};
