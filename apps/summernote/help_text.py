from .settings import RESIZE_WIDTH
help_text = f'\
        <p>アップロードする画像は幅が {RESIZE_WIDTH}px を超える場合にはこれに縮小されます。</p>\
        <div class="badge rounded-pill text-bg-info mt-3" href="#SummerNoteTextAreaHelpText" data-bs-toggle="collapse" aria-expanded="false" aria-controls="SummerNoteTextAreaHelpText">summernote helper<i class="fa-solid fa-up-right-and-down-left-from-center m-1"></i></div>\
        <div class="collapse multi-collapse pt-2" id="SummerNoteTextAreaHelpText">\
        <div class="list-group list-group-flush ms-2">\
        <div class="list-group-item mt-2 ms-2"><kbd>SHIFT</kbd>+<kbd>ENTER</kbd> :装飾を残したまま改行</div>\
        <div class="list-group-item mt-2 ms-2"><kbd>@</kbd>+<kbd>any words</kbd> :メンション</div>\
        <div class="list-group-item mt-2 ms-2"><kbd>:</kbd>+<kbd>alphabet</kbd>  :絵文字 [ <a class="link-info" href="https://github.com/ikatyang/emoji-cheat-sheet/" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-up-right-from-square"></i>cheat sheet</a> ]</div>\
        </div></div>'