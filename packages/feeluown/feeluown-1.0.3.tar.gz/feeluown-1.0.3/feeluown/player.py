# -*- coding: utf-8 -*-

import asyncio
import logging
import random

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot

from .model import SongModel
from .consts import PlaybackMode


logger = logging.getLogger(__name__)


class Player(QMediaPlayer):
    signal_player_media_changed = pyqtSignal([SongModel])
    signal_playlist_is_empty = pyqtSignal()
    signal_playback_mode_changed = pyqtSignal([PlaybackMode])
    signal_playlist_finished = pyqtSignal()

    signal_song_required = pyqtSignal()
    finished = pyqtSignal()

    _music_list = list()    # 里面的对象是music_model
    _current_index = None
    _tmp_fix_next_song = None
    playback_mode = PlaybackMode.loop
    last_playback_mode = PlaybackMode.loop
    _other_mode = False

    def __init__(self, app):
        super().__init__(app)
        self._app = app

        self.error.connect(self.on_error_occured)
        self.mediaChanged.connect(self.on_media_changed)
        self.mediaStatusChanged.connect(self.on_media_status_changed)

        self._music_error_times = 0

        # latency of retying next operation when error happened
        self._retry_latency = 3
        # when _music_error_times reached _music_error_maximum, play next music
        self._music_error_maximum = 3

    def change_player_mode_to_normal(self):
        logger.debug('退出特殊的播放模式')
        self._other_mode = False
        self._set_playback_mode(self.last_playback_mode)

    def change_player_mode_to_other(self):
        # player mode: such as fm mode, different from playback mode
        logger.debug('进入特殊的播放模式')
        self._other_mode = True
        self._set_playback_mode(PlaybackMode.sequential)

    def _record_playback_mode(self):
        self.last_playback_mode = self.playback_mode

    @pyqtSlot(QMediaContent)
    def on_media_changed(self, media_content):
        music_model = self._music_list[self._current_index]
        self.signal_player_media_changed.emit(music_model)

    @pyqtSlot(QMediaPlayer.MediaStatus)
    def on_media_status_changed(self, state):
        if state == QMediaPlayer.EndOfMedia:
            self.finished.emit()
            self.stop()
            if (self._current_index == len(self._music_list) - 1) and\
                    self._other_mode:
                self.signal_playlist_finished.emit()
                logger.debug("播放列表播放完毕")
            if not self._other_mode:
                self.play_next()
        # TODO: at hotkey linux module, when it call
        #       Controller.player.play_next or last may stop the player
        #       add following code to fix the problem.
        elif state in (QMediaPlayer.LoadedMedia, ):
            self.play()

    def insert_to_next(self, model):
        if not self.is_music_in_list(model):
            if self._current_index is None:
                index = 0
            else:
                index = self._current_index + 1
            self._music_list.insert(index, model)
            return True
        return False

    def add_music(self, song):
        self._music_list.append(song)

    def remove_music(self, mid):
        for i, music_model in enumerate(self._music_list):
            if mid == music_model.mid:
                self._music_list.pop(i)
                if i == self._current_index:
                    self.play_next()
                elif i < self._current_index:
                    self._current_index -= 1
                return True
        return False

    def get_media_content_from_model(self, music_model):
        url = music_model.url
        if not url:
            self._app.message('URL 不存在，不能播放该歌曲')
            return None
        if url.startswith('http'):
            media_content = QMediaContent(QUrl(url))
        else:
            media_content = QMediaContent(QUrl.fromLocalFile(url))
        return media_content

    def set_music_list(self, music_list):
        self._music_list = []
        self._music_list = music_list
        if len(self._music_list):
            self.play(self._music_list[0])

    def clear_playlist(self):
        self._music_list = []
        self._current_index = 0
        self.stop()

    def is_music_in_list(self, model):
        for music in self._music_list:
            if model.mid == music.mid:
                return True
        return False

    def _play(self, music_model):
        insert_flag = self.insert_to_next(music_model)
        index = self.get_index_by_model(music_model)
        if not insert_flag and self._current_index is not None:
            if music_model.mid == self._music_list[self._current_index].mid\
                    and self.state() == QMediaPlayer.PlayingState:
                return True
        super().stop()
        media_content = self.get_media_content_from_model(music_model)
        if media_content is not None:
            logger.debug('start to play song: %d, %s, %s' %
                         (music_model.mid, music_model.title, music_model.url))
            self._current_index = index
            self.setMedia(media_content)
            super().play()
            return True
        else:
            self.remove_music(music_model.mid)
            self.play_next()
            return False

    def other_mode_play(self, music_model):
        self._play(music_model)

    def play(self, music_model=None):
        if music_model is None:
            super().play()
            return False
        self._app.player_mode_manager.exit_to_normal()
        self._play(music_model)

    def get_index_by_model(self, music_model):
        for i, music in enumerate(self._music_list):
            if music_model.mid == music.mid:
                return i
        return None

    def play_or_pause(self):
        if len(self._music_list) is 0:
            self.signal_playlist_is_empty.emit()
            return
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        elif self.state() == QMediaPlayer.PausedState:
            self.play()
        else:
            self.play_next()

    def play_next(self):
        if self._tmp_fix_next_song is not None:
            flag = self.play(self._tmp_fix_next_song)
            self._tmp_fix_next_song = None
            return flag
        index = self.get_next_song_index()
        if index is not None:
            if index == 0 and self._other_mode:
                self.signal_playlist_finished.emit()
                logger.debug("播放列表播放完毕")
                return
            music_model = self._music_list[index]
            self.play(music_model)
            return True
        else:
            self.signal_playlist_is_empty.emit()
            return False

    def play_last(self):
        index = self.get_previous_song_index()
        if index is not None:
            music_model = self._music_list[index]
            self.play(music_model)
            return True
        else:
            self.signal_playlist_is_empty.emit()
            return False

    def set_tmp_fixed_next_song(self, song):
        self._tmp_fix_next_song = song

    @pyqtSlot(QMediaPlayer.Error)
    def on_error_occured(self, error):
        song = self._music_list[self._current_index]
        self._app.message('cant play song: %s' % (song.title))
        self.stop()
        if error == QMediaPlayer.FormatError:
            self._app.message('这首歌挂了，也有可能是断网了', error=True)
            logger.debug('song cant be played, url is %s' % song.url)
        elif error == QMediaPlayer.NetworkError:
            self._wait_to_retry()
        elif error == QMediaPlayer.ResourceError:
            logger.error('网络出现错误：不能正确解析资源')
        elif error == QMediaPlayer.ServiceMissingError:
            self._app.notify('缺少解码器，请向作者求助', error=True)
        else:
            self._wait_to_next(2)

    def _wait_to_retry(self):
        if self._music_error_times >= self._music_error_maximum:
            self._music_error_times = 0
            self._wait_to_next(self._retry_latency)
            self._app.message('将要播放下一首歌曲', error=True)
        else:
            self._music_error_times += 1
            app_event_loop = asyncio.get_event_loop()
            app_event_loop.call_later(self._retry_latency, self.play)
            self._app.message('网络连接不佳', error=True)

    def _wait_to_next(self, second=0):
        if len(self._music_list) < 2:
            return
        app_event_loop = asyncio.get_event_loop()
        app_event_loop.call_later(second, self.play_next)

    def get_next_song_index(self):
        if len(self._music_list) is 0:
            self._app.message('当前播放列表没有歌曲')
            return None
        if self.playback_mode == PlaybackMode.one_loop:
            return self._current_index
        elif self.playback_mode == PlaybackMode.loop:
            if self._current_index >= len(self._music_list) - 1:
                return 0
            else:
                return self._current_index + 1
        elif self.playback_mode == PlaybackMode.sequential:
            return None
        else:
            return random.choice(range(len(self._music_list)))

    def get_previous_song_index(self):
        if len(self._music_list) is 0:
            return None
        if self.playback_mode == PlaybackMode.one_loop:
            return self._current_index
        elif self.playback_mode == PlaybackMode.loop:
            if self._current_index is 0:
                return len(self._music_list) - 1
            else:
                return self._current_index - 1
        elif self.playback_mode == PlaybackMode.sequential:
            return None
        else:
            return random.choice(range(len(self._music_list)))

    def _set_playback_mode(self, mode):
        # item once: 0
        # item in loop: 1
        # sequential: 2
        # loop: 3
        # random: 4
        if mode == self.playback_mode:
            return 0
        self._record_playback_mode()
        self.playback_mode = mode
        self._app.message('设置播放顺序为：%s' % mode.value)
        self.signal_playback_mode_changed.emit(mode)

    def next_playback_mode(self):
        if self.playback_mode == PlaybackMode.one_loop:
            self._set_playback_mode(PlaybackMode.loop)
        elif self.playback_mode == PlaybackMode.loop:
            self._set_playback_mode(PlaybackMode.random)
        elif self.playback_mode == PlaybackMode.random:
            self._set_playback_mode(PlaybackMode.one_loop)

    @property
    def songs(self):
        return self._music_list
