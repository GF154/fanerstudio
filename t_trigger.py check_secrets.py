[33mcommit 6ad76236d1885c7e278623c6a76c68c740f5e9df[m[33m ([m[1;31morigin/main[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: Fanerlink <fanerlink@kreyolia.ht>
Date:   Sun Oct 26 16:22:45 2025 -0400

    feat: Complete voiceover correction modal with AI error detection

[1mdiff --git a/tools.html b/tools.html[m
[1mindex aa40e5b..9b40bfe 100644[m
[1m--- a/tools.html[m
[1m+++ b/tools.html[m
[36m@@ -738,8 +738,8 @@[m
                 <div class="tool-card" onclick="openModal('video-correct')">[m
                     <div class="tool-icon">🔧</div>[m
                     <h3>Korije Erè Vwadeyò</h3>[m
[31m-                    <p>Korije erè ak kòreksyon paròl nan videyo.</p>[m
[31m-                    <span class="badge dev">Dev</span>[m
[32m+[m[32m                    <p>Korije erè ak pwoblèm nan vwadeyò videyo ou.</p>[m
[32m+[m[32m                    <span class="badge ready">Ready</span>[m
                 </div>[m
 [m
                 <div class="tool-card" onclick="openModal('music-ai')">[m
[36m@@ -1178,8 +1178,95 @@[m
                 `[m
             },[m
             'video-correct': {[m
[31m-                title: '🔧 Korije Erè Vwadeyò',[m
[31m-                form: `<button class="btn-primary" disabled>Pral Disponib Byento</button>`[m
[32m+[m[32m                title: 'Korije Erè Vwadeyò',[m
[32m+[m[32m                form: `[m
[32m+[m[32m                    <p style="color: #718096; margin-bottom: 24px; font-size: 0.95em;">Korije erè ak pwoblèm nan vwadeyò videyo ou. Reyenrejistre seksyon ki gen pwoblèm yo.</p>[m
[32m+[m[41m                    [m
[32m+[m[32m                    <!-- Upload Video -->[m
[32m+[m[32m                    <div class="form-group">[m
[32m+[m[32m                        <label style="font-weight: 600; color: #2d3748; margin-bottom: 12px;">Telechaje videyo ak vwadeyò</label>[m
[32m+[m[32m                        <div class="upload-zone" onclick="document.getElementById('correct-video').click()">[m
[32m+[m[32m                            <div class="upload-icon">🎬</div>[m
[32m+[m[32m                            <div class="upload-text">Klike pou telechaje videyo, oswa trennen epi lage</div>[m
[32m+[m[32m                            <div class="upload-formats">.mp4, .mov, .avi, .mkv, .webm</div>[m
[32m+[m[32m                            <input type="file" id="correct-video" accept="video/*" style="display: none;">[m
[32m+[m[32m                        </div>[m
[32m+[m[32m                    </div>[m
[32m+[m[41m                    [m
[32m+[m[32m                    <!-- Detection Method -->[m
[32m+[m[32m                    <div class="form-group">[m
[32m+[m[32m                        <label style="font-weight: 600; color: #2d3748; margin-bottom: 12px;">Metòd deteksyon erè</label>[m
[32m+[m[32m                        <select class="voice-select">[m
[32m+[m[32m                            <option value="auto">🔍 Otomatik (IA detekte erè)</option>[m
[32m+[m[32m                            <option value="manual">✏️ Manyèl (ou chwazi seksyon yo)</option>[m
[32m+[m[32m                            <option value="transcript">📝 Konpare ak transkripsyon</option>[m
[32m+[m[32m                        </select>[m
[32m+[m[32m                    </div>[m
[32m+[m[41m                    [m
[32m+[m[32m                    <!-- Error Types to Detect -->[m
[32m+[m[32m                    <div class="form-group">[m
[32m+[m[32m                        <label style="font-weight: 600; color: #2d3748; margin-bottom: 12px;">Tip erè pou detekte</label>[m
[32m+[m[32m                        <div style="background: #f7fafc; border: 2px solid #e2e8f0; border-radius: 8px; padding: 16px;">[m
[32m+[m[32m                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer; margin-bottom: 8px;">[m
[32m+[m[32m                                <input type="checkbox" id="error-pronunciation" style="width: auto; cursor: pointer;" checked>[m
[32m+[m[32m                                <span>Pwononsyasyon move</span>[m
[32m+[m[32m                            </label>[m
[32m+[m[32m                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer; margin-bottom: 8px;">[m
[32m+[m[32m                                <input type="checkbox" id="error-timing" style="width: auto; cursor: pointer;" checked>[m
[32m+[m[32m                                <span>Pwoblèm timing (desenkwonizasyon)</span>[m
[32m+[m[32m                            </label>[m
[32m+[m[32m                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer; margin-bottom: 8px;">[m
[32m+[m[32m                                <input type="checkbox" id="error-words" style="width: auto; cursor: pointer;" checked>[m
[32m+[m[32m                                <span>Mo ki pa kòrèk</span>[m
[32m+[m[32m                            </label>[m
[32m+[m[32m                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer;">[m
[32m+[m[32m                                <input type="checkbox" id="error-audio" style="width: auto; cursor: pointer;">[m
[32m+[m[32m                                <span>Kalite odyo ki move</span>[m
[32m+[m[32m                            </label>[m
[32m+[m[32m                        </div>[m
[32m+[m[32m                    </div>[m
[32m+[m[41m                    [m
[32m+[m[32m                    <!-- Correction Voice -->[m
[32m+[m[32m                    <div class="form-group">[m
[32m+[m[32m                        <label style="font-weight: 600; color: #2d3748; margin-bottom: 12px;">Vwa pou kòreksyon yo</label>[m
[32m+[m[32m                        <select class="voice-select">[m
[32m+[m[32m                            <option value="original">🔄 Menm vwa orijinal la</option>[m
[32m+[m[32m                            <option value="kreyol-natif">🇭🇹 Kreyòl Natif Natal</option>[m
[32m+[m[32m                            <option value="le-glacial">🎭 Le Glacial</option>[m
[32m+[m[32m                            <option value="custom">🎙️ Anrejistre nouvo vwa</option>[m
[32m+[m[32m                        </select>[m
[32m+[m[32m                    </div>[m
[32m+[m[41m                    [m
[32m+[m[32m                    <!-- Correction Options -->[m
[32m+[m[32m                    <div class="form-group" style="margin-bottom: 8px;">[m
[32m+[m[32m                        <label style="font-weight: 600; color: #2d3748; margin-bottom: 12px;">Opsyon kòreksyon</label>[m
[32m+[m[41m                        [m
[32m+[m[32m                        <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer; margin-bottom: 8px;">[m
[32m+[m[32m                            <input type="checkbox" id="smooth-transitions" style="width: auto; cursor: pointer;" checked>[m
[32m+[m[32m                            <span>Tranzisyon smooth ant seksyon yo</span>[m
[32m+[m[32m                        </label>[m
[32m+[m[41m                        [m
[32m+[m[32m                        <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer; margin-bottom: 8px;">[m
[32m+[m[32m                            <input type="checkbox" id="match-tone" style="width: auto; cursor: pointer;" checked>[m
[32m+[m[32m                            <span>Adapte ton ak vwadeyò orijinal la</span>[m
[32m+[m[32m                        </label>[m
[32m+[m[41m                        [m
[32m+[m[32m                        <label style="display: flex; align-items: center; gap: 8px; font-size: 0.95em; color: #4a5568; cursor: pointer;">[m
[32m+[m[32m                            <input type="checkbox