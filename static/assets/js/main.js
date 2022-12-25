/**
* Template Name: NiceAdmin - v2.4.1
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */
  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

  tinymce.init({
    selector: 'textarea.tinymce-editor',
    plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons',
    editimage_cors_hosts: ['picsum.photos'],
    menubar: 'file edit view insert format tools table help',
    toolbar: 'undo redo | bold italic underline strikethrough | fontfamily fontsize blocks | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
    toolbar_sticky: true,
    toolbar_sticky_offset: isSmallScreen ? 102 : 108,
    autosave_ask_before_unload: true,
    autosave_interval: '30s',
    autosave_prefix: '{path}{query}-{id}-',
    autosave_restore_when_empty: false,
    autosave_retention: '2m',
    image_advtab: true,
    link_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_class_list: [{
        title: 'None',
        value: ''
      },
      {
        title: 'Some class',
        value: 'class-name'
      }
    ],
    importcss_append: true,
    file_picker_callback: (callback, value, meta) => {
      /* Provide file and text for the link dialog */
      if (meta.filetype === 'file') {
        callback('https://www.google.com/logos/google.jpg', {
          text: 'My text'
        });
      }

      /* Provide image and alt text for the image dialog */
      if (meta.filetype === 'image') {
        callback('https://www.google.com/logos/google.jpg', {
          alt: 'My alt text'
        });
      }

      /* Provide alternative source and posted for the media dialog */
      if (meta.filetype === 'media') {
        callback('movie.mp4', {
          source2: 'alt.ogg',
          poster: 'https://www.google.com/logos/google.jpg'
        });
      }
    },
    templates: [{
        title: 'New Table',
        description: 'creates a new table',
        content: '<div class="mceTmpl"><table width="98%%"  border="0" cellspacing="0" cellpadding="0"><tr><th scope="col"> </th><th scope="col"> </th></tr><tr><td> </td><td> </td></tr></table></div>'
      },
      {
        title: 'Starting my story',
        description: 'A cure for writers block',
        content: 'Once upon a time...'
      },
      {
        title: 'New list with dates',
        description: 'New List with dates',
        content: '<div class="mceTmpl"><span class="cdate">cdate</span><br><span class="mdate">mdate</span><h2>My List</h2><ul><li></li><li></li></ul></div>'
      }
    ],
    template_cdate_format: '[Date Created (CDATE): %m/%d/%Y : %H:%M:%S]',
    template_mdate_format: '[Date Modified (MDATE): %m/%d/%Y : %H:%M:%S]',
    height: 600,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    contextmenu: 'link image table',
    skin: useDarkMode ? 'oxide-dark' : 'oxide',
    content_css: useDarkMode ? 'dark' : 'default',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
  });

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable);
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }
  function getDate(){
    var today = new Date();

document.getElementById("date").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);


}

})();

var date = new Date();

var day = date.getDate();
var month = date.getMonth() + 1;
var year = date.getFullYear();

if (month < 10) month = "0" + month;
if (day < 10) day = "0" + day;

var today = year + "-" + month + "-" + day;       
document.getElementById("date").value = today;

function toggle(source) {
  checkboxes = document.getElementsByName('attendance1');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}
// $(document).ready(function(){

// $("#table table-borderless datatable").DataTable({
//   'paging':false
// });


// });
$(function(){
  $("#table table-borderless datatable").DataTable({
    "paging":false,
    "pageLength":1
  })
}
)

function check_absent_or_leave(){
  val = document.getElementsByName('attendance').value;
  yy=document.querySelector('attendance').checked;
  alert(yy);
  // window.alert('fhhh');
  // document.getElementsByName('test1').text()='dhdh';


}


// my extra added code to sort number and text column in a table

(function(){
  function findAncestor (el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
  }
  
  function unformatNumberString(number) {
    number = number.replace(/[^\d\.-]/g, '');
    return Number(number);
  }
  
  function extractStringContent(s) {
    var span = document.createElement('span');
    span.innerHTML = s;
    return span.textContent || span.innerText;
  };
  
  function setColHeaderDirection(newDirection, colIndex, colHeaders) {
    for (let index = 0; index < colHeaders.length; index++) {
      if(index == colIndex) {
        colHeaders[colIndex].setAttribute("data-sort-direction", newDirection);
      } else {
        colHeaders[index].setAttribute("data-sort-direction", 0);
      }
    }
  }
  
  function renderSortedTable(table, data) {
    let tableRows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    for (let rowIndex = 0; rowIndex < tableRows.length; rowIndex++) {
      let tableRowCells = tableRows[rowIndex].getElementsByTagName("td");
      for (let cellIndex = 0; cellIndex < tableRowCells.length; cellIndex++) {
        tableRowCells[cellIndex].innerHTML = data[rowIndex][cellIndex];
      }
    }
  }

  window.addEventListener('load', function() {
    var sortableTables = document.getElementsByClassName("sortable-table");
    var tablesData = [];
    for (let tableIndex = 0; tableIndex < sortableTables.length; tableIndex++) {
      sortableTables[tableIndex].setAttribute("data-sort-index", tableIndex);
      // fill tablesData
      let tableRows = sortableTables[tableIndex].getElementsByTagName("tbody")[0].getElementsByTagName("tr");
      for (let rowIndex = 0; rowIndex < tableRows.length; rowIndex++) {
        let tableRowCells = tableRows[rowIndex].getElementsByTagName("td");
        for (let cellIndex = 0; cellIndex < tableRowCells.length; cellIndex++) {
          if (tablesData[tableIndex] === void 0) {
            tablesData.splice(tableIndex, 0, []);
          }
          if (tablesData[tableIndex][rowIndex] === void 0) {
            tablesData[tableIndex].splice(rowIndex, 0, []);
          }
          tablesData[tableIndex][rowIndex].splice(cellIndex, 0, tableRowCells[cellIndex].innerHTML)
        }
      }
  
      // bind headers to event
      let tableHeaders = sortableTables[tableIndex].getElementsByTagName("thead")[0].getElementsByTagName("tr")[0].getElementsByTagName("th");
      for (let headerIndex = 0; headerIndex < tableHeaders.length; headerIndex++) {
        let colIsNumeric = tableHeaders[headerIndex].classList.contains("numeric-sort");
        tableHeaders[headerIndex].setAttribute("data-sort-direction", 0);
        tableHeaders[headerIndex].setAttribute("data-sort-index", headerIndex);
        // Header Click Event
        tableHeaders[headerIndex].addEventListener('click', function() {
          let colSortDirection = this.getAttribute("data-sort-direction");
          let headerIndex = this.getAttribute("data-sort-index");
          let tableIndex = findAncestor(this, "sortable-table").getAttribute("data-sort-index");
          if(colSortDirection == 1) {
            setColHeaderDirection(-1, headerIndex, tableHeaders)
          } else {
            setColHeaderDirection(1, headerIndex, tableHeaders)
          }
          tablesData[tableIndex] = tablesData[tableIndex].sort(function(a,b) {
            let x = extractStringContent(a[headerIndex]);
            let y = extractStringContent(b[headerIndex]);
            if(colIsNumeric) {
              x = unformatNumberString(x);
              y = unformatNumberString(y);
            }
  
            if (x === y) {
              return 0;
            }
            else {
              if(colSortDirection == 1) { // it was up and now it's down
                return (x > y) ? -1 : 1;
              } else {
                return (x < y) ? -1 : 1;
              }
            }
          });
          renderSortedTable(sortableTables[tableIndex], tablesData[tableIndex]);
        });
      }
    }
  });
})();





// var date = new Date();

// var day = date.getDate();
// var month = date.getMonth() + 1;
// var year = date.getFullYear();

// if (month < 10) month = "0" + month;
// if (day < 10) day = "0" + day;

// var today = year + "-" + month + "-" + day;       
// document.getElementById("date_today_auto").value = today;