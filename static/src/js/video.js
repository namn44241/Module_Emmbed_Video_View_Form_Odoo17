/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { Component, onMounted, useRef, xml } from "@odoo/owl";

class VideoPlayer extends Component {
    static template = xml`
        <div class="o_video_container">
            <div t-ref="youtubePlayer" class="youtube-player"></div>
        </div>
    `;

    static props = {
        videoId: { type: String, optional: true },
    };

    setup() {
        this.youtubePlayerRef = useRef("youtubePlayer");
        this.player = null;
        
        onMounted(() => {
            this._loadYoutubeAPI().then(() => {
                this._setupYoutubePlayer();
            });
        });
    }

    _loadYoutubeAPI() {
        const youtubeUrl = 'https://www.youtube.com/iframe_api';
        
        return new Promise((resolve) => {
            if (document.querySelector(`script[src="${youtubeUrl}"]`)) {
                if (window.YT && window.YT.Player) {
                    resolve();
                } else {
                    window.onYouTubeIframeAPIReady = () => resolve();
                }
                return;
            }
            
            const script = document.createElement('script');
            script.src = youtubeUrl;
            script.async = true;
            
            window.onYouTubeIframeAPIReady = () => resolve();
            
            document.head.appendChild(script);
        });
    }

    _setupYoutubePlayer() {
        if (!this.youtubePlayerRef.el) return;
        
        this.player = new YT.Player(this.youtubePlayerRef.el, {
            videoId: this.props.videoId,
            playerVars: {
                'autoplay': 0,
                'origin': window.location.origin,
                'rel': 0
            },
            events: {
                'onStateChange': this._onPlayerStateChange.bind(this)
            }
        });
    }

    _onPlayerStateChange(event) {
    }
}

registry.category("public_components").add("videoPlayer", VideoPlayer);

export default VideoPlayer;