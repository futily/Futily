<template>
  <form :class="['bld-Builder', `bld-Builder-${formation}`]" @submit="handleSubmit">
    <header class="bld-Builder_Header">
      <BuilderStats />
    </header>

    <div class="bld-Builder_Body">
      <div class="bld-Builder_Team">
        <canvas class="bld-Builder_Canvas" ref="canvas"></canvas>

        <ul class="bld-Builder_Players">
          <li :class="getTeamPlayerClass(player)"
              v-for="player in players.team"
              :key="player.index"
              ref="team">
            <BuilderSlot :player="player" />
          </li>
        </ul>

        <BuilderSearch v-if="isEditable" />
      </div>

      <div class="bld-Builder_ExtraPlayers">
        <div class="bld-ExtraPlayers">
          <div class="bld-ExtraPlayers_Inner">
            <div class="bld-ExtraPlayers_Body">
              <div class="bld-ExtraPlayers_Bench">
                <p class="bld-ExtraPlayers_Title">Bench</p>

                <ul class="bld-ExtraPlayers_Items">
                  <li class="bld-ExtraPlayers_Item"
                      v-for="player in players.bench"
                      :key="player.index">
                    <BuilderSlot :player="player" />
                  </li>
                </ul>
              </div>

              <div class="bld-ExtraPlayers_Reserves">
                <p class="bld-ExtraPlayers_Title">Reserves</p>

                <ul class="bld-ExtraPlayers_Items">
                  <li class="bld-ExtraPlayers_Item"
                      v-for="player in players.reserves"
                      :key="player.index">
                    <BuilderSlot :player="player" />
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
  import Draggable from '@shopify/draggable/lib/draggable';
  import { mapActions, mapGetters, mapMutations } from 'vuex';

  import BuilderSearch from './BuilderSearch.vue';
  import BuilderSlot from './BuilderSlot.vue';
  import BuilderStats from './BuilderStats.vue';
  import * as types from '../types';

  export default {
    components: {
      BuilderSearch,
      BuilderSlot,
      BuilderStats,
    },

    props: {
      defaultFormation: {
        type: String,
        default: '442',
      },
      page: Number,
      saveUrl: String,
    },

    data () {
      return {
        dragStartIndex: null,
        dragOverIndex: null,
      };
    },

    mounted () {
      this.setup({
        elements: {
          team: this.$refs.team,
        },
        page: this.page,
      });

      this.initCanvas();
      this.setupListeners();
    },

    computed: {
      ...mapGetters({
        'chemLinks': types.GET_CHEMLINKS,
        'filledTeamIndexes': types.GET_FILLED_TEAM_INDEXES,
        'formation': types.GET_FORMATION,
        'isEditable': types.GET_IS_EDITABLE,
        'players': types.GET_PLAYERS,
        'stats': types.GET_STATS,
      }),
    },

    watch: {
      formation () {
        this.$nextTick(() => {
          this.initCanvas();
        });
      },

      'filledTeamIndexes' (val) {
        this.$nextTick(() => {
          this.initCanvas();
        });
      },
    },

    methods: {
      ...mapActions({
        'initialise': types.INITIALISE,
        'insertPlayer': types.INSERT_PLAYER,
        'removePlayer': types.REMOVE_PLAYER,
        'setup': types.SETUP,
        'setFormation': types.SET_FORMATION,
      }),

      clearCanvas () {
        const canvas = this.$refs.canvas;
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
      },

      drawLine (start, end, chemistry) {
        const context = this.$refs.canvas.getContext('2d');
        const color =
          chemistry >= 2 ? '#a5f35c' : chemistry >= 1 ? '#cf8600' : '#a31a19';
        context.lineWidth = 3;
        context.strokeStyle = color;
        context.lineCap = 'round';
        context.shadowOffsetY = 1.5;
        context.shadowColor = 'rgba(0, 0, 0, 0.5)';
        context.shadowBlur = 1.5;
        context.beginPath();
        context.moveTo(start.x, start.y);
        context.lineTo(end.x, end.y);
        context.stroke();
      },

      initCanvas () {
        this.clearCanvas();

        this.chemLinks.map(link => {
          const player = this.players.team[link.a];
          const target = this.players.team[link.b];

          this.drawLine(
            player.getCoordinates(),
            target.getCoordinates(),
            player.calculateIndividualLinkChemistry(target),
          );
        });
      },

      getTeamPlayerClass (player) {
        return [
          'bld-Builder_PlayersItem',
          {
            [`bld-Builder_PlayersItem-${player.positions.verbose.toLowerCase()}`]: player.positions.verbose,
            'bld-Builder_PlayersItem-draggable': player.isFilled,
          },
        ];
      },

      async handleSubmit (evt) {
        evt.preventDefault();

        const data = new FormData(this.$el);

        const res = await this.$http({
          data,
          method: 'POST',
          url: this.saveUrl,
          xsrfCookieName: 'csrftoken',
          xsrfHeaderName: 'X-CSRFToken',
        });

        if (res.status === 200) {
          window.location.href = res.data.url;
        }
      },

      setupListeners () {
        this.handleDragStop = this.handleDragStop.bind(this);
        this.handleDragMove = this.handleDragMove.bind(this);
        this.handleDragStart = this.handleDragStart.bind(this);
        const draggable = new Draggable(this.$refs.team, {
          draggable: `.bld-Builder_PlayersItem-draggable`,
        });
        draggable.on('drag:start', this.handleDragStart);
        draggable.on('drag:move', this.handleDragMove);
        draggable.on('drag:stop', this.handleDragStop);
      },

      handleDragStart (evt) {
        this.dragStartIndex = this.$refs.team.indexOf(evt.data.originalSource);
      },

      handleDragMove (evt) {
        const target = evt.sensorEvent.data.target.closest('.bld-Builder_PlayersItem');

        this.dragOverIndex = this.$refs.team.includes(target)
          ? this.$refs.team.indexOf(target)
          : null;
      },

      handleDragStop () {
        if (this.dragStartIndex === null || this.dragOverIndex === null) return;
        const sourcePlayer = this.players.team[this.dragStartIndex];
        const targetPlayer = this.players.team[this.dragOverIndex];

        const sourceObj = {
          data: sourcePlayer.data,
          index: this.dragStartIndex,
        };
        const targetObj = {
          data: targetPlayer.isFilled ? targetPlayer.data : {},
          index: this.dragOverIndex,
        };

        if (targetPlayer.isFilled) {
          this.removePlayer({ index: sourceObj.index });
          this.removePlayer({ index: targetObj.index });

          this.insertPlayer({ index: sourceObj.index, data: targetObj.data });
          this.insertPlayer({ index: targetObj.index, data: sourceObj.data });
        } else {
          this.removePlayer({ index: sourceObj.index });
          this.insertPlayer({ index: targetObj.index, data: sourceObj.data });
        }
      },
    },
  };
</script>
