import axios from 'axios';

export class Follow {
  constructor ({ el }) {
    this.el = el;
    this.termEl = el.querySelector('.js-UserFollow_Term');
    this.followersEl = document.querySelector('.js-UserFollow_Followers');
    this._followersCount = Number(this.followersEl.innerText);
    this.url = this.el.dataset.action;
    this._isFollowing = this.el.dataset.isFollowing === 'true';

    this.handleClick = this.handleClick.bind(this);

    this.setupListeners();
  }

  setupListeners () {
    this.el.addEventListener('pointerdown', this.handleClick);
  }

  handleClick () {
    axios
      .post(
        this.url,
        {},
        {
          xsrfCookieName: 'csrftoken',
          xsrfHeaderName: 'X-CSRFToken',
        }
      )
      .then(res => {
        this.isFollowing = res.data.followed;
      });
  }

  get isFollowing () {
    return this._isFollowing;
  }

  set isFollowing (val) {
    this._isFollowing = val;

    this.termEl.innerText = val ? 'Following' : 'Follow';
    this.followersCount = val
      ? this.followersCount + 1
      : this.followersCount - 1;
  }

  get followersCount () {
    return this._followersCount;
  }

  set followersCount (val) {
    this._followersCount = val;

    this.followersEl.innerText = val;
  }
}
