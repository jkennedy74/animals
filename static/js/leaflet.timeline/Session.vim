let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
let EasyMotion_off_screen_search =  1 
let AutoPairsMapBS =  1 
let EasyMotion_move_highlight =  1 
let AutoPairsShortcutBackInsert = "<M-b>"
let AutoPairsLoaded =  1 
let EditorConfig_preserve_formatoptions =  0 
let AutoPairsShortcutToggle = "<M-p>"
let EasyMotion_smartcase =  0 
let AutoPairsMapCR =  1 
let AutoPairsMapCh =  1 
let EasyMotion_enter_jump_first =  0 
let EditorConfig_exec_path = ""
let EasyMotion_use_upper =  0 
let EasyMotion_do_mapping =  1 
let Taboo_tabs = "1	build\n2	Code\n3	Tests\n"
let AutoPairsSmartQuotes =  1 
let EasyMotion_disable_two_key_combo =  0 
let EasyMotion_space_jump_first =  0 
let EasyMotion_prompt = "Search for {n} character(s): "
let EasyMotion_use_regexp =  1 
let AutoPairsShortcutFastWrap = "<M-e>"
let EditorConfig_max_line_indicator = "line"
let EasyMotion_show_prompt =  1 
let EasyMotion_add_search_history =  1 
let EasyMotion_do_shade =  1 
let NetrwMenuPriority =  80 
let EasyMotion_grouping =  1 
let EasyMotion_inc_highlight =  1 
let EasyMotion_skipfoldedline =  1 
let EasyMotion_use_migemo =  0 
let EditorConfig_python_files_dir = "plugin/editorconfig-core-py"
let EasyMotion_verbose =  1 
let AutoPairsMultilineClose =  1 
let EditorConfig_verbose =  0 
let AutoPairsShortcutJump = "<M-n>"
let AutoPairsMapSpace =  1 
let EasyMotion_cursor_highlight =  1 
let AutoPairsFlyMode =  0 
let EasyMotion_startofline =  1 
let AutoPairsCenterLine =  1 
let EasyMotion_keys = "asdghklqwertyuiopzxcvbnmfj;"
let EasyMotion_force_csapprox =  0 
let EasyMotion_loaded =  1 
let NetrwTopLvlMenu = "Netrw."
let BufExplorer_title = "[Buf List]"
let AutoPairsMoveCharacter = "()[]{}\"'"
let EasyMotion_landing_highlight =  0 
silent only
cd ~/Code/Leaflet.timeline
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 ~/Code/Leaflet.timeline
badd +68 package.json
badd +1 test/Timeline_test.js
badd +39 karma.conf.js
badd +11 .travis.yml
badd +1 src
badd +455 src/TimelineSliderControl.js
badd +26 webpack.config.js
badd +4 test/TimeSliderControl_test.js
badd +65 examples/borders.html
badd +1 test/.tern-project
badd +1 test/.eslintrc
badd +1 test/TimeSliderControl.test.js
badd +0 test/Timeline.spec.js
argglobal
silent! argdel *
edit package.json
set splitbelow splitright
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
2
normal! zo
let s:l = 8 - ((7 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
8
normal! 017|
lcd ~/Code/Leaflet.timeline
tabnew
set splitbelow splitright
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
tabedit ~/Code/Leaflet.timeline/test/Timeline.spec.js
set splitbelow splitright
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
8
normal! zo
9
normal! zo
9
normal! zc
let s:l = 1 - ((0 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd ~/Code/Leaflet.timeline
tabnext 2
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=atI
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
let g:this_session = v:this_session
let g:this_obsession = v:this_session
let g:this_obsession_status = 2
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
