from modal_3 import BASE_ROOT, list_files_and_folders, get_breadcrumb_path, get_current_path_from_url, is_safe_path


def generate_file_list_html(files, current_path="wwwroot"):
    """Dosya listesi için HTML tablosu oluşturur"""
    html = ""
    
    for file in files:
        file_type = "folder" if file['is_dir'] else "file"
        icon_class = "text-primary" if file['is_dir'] else "text-subtle-light dark:text-subtle-dark"
        
        # Dosya/klasör path'ini oluştur
        file_path = f"{current_path}/{file['name']}"
        # URL path'ini oluştur - BASE_ROOT'u kaldır
        if current_path == BASE_ROOT:
            file_url_path = f"/{file['name']}"
        else:
            file_url_path = f"/{current_path.replace(BASE_ROOT + '/', '')}/{file['name']}"
        
        # Klasörler için tıklanabilir link ekle
        if file['is_dir']:
            html += f'''
                <tr class="hover:bg-primary/5 dark:hover:bg-primary/10 transition-colors duration-150 cursor-pointer"
                    data-type="{file_type}" data-path="{file_path}" data-url-path="{file_url_path}" data-name="{file['name']}" onclick="window.location.href='{file_url_path}'">
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                            <span class="material-symbols-outlined mr-3 {icon_class}">{file['icon']}</span>
                            <div class="text-sm font-medium">{file['name']}</div>
                        </div>
                    </td>
                    <td class="hidden px-6 py-4 whitespace-nowrap text-sm text-subtle-light dark:text-subtle-dark md:table-cell">
                        {file['modified']}
                    </td>
                    <td class="hidden px-6 py-4 whitespace-nowrap text-sm text-subtle-light dark:text-subtle-dark lg:table-cell">
                        {file['size']}
                    </td>
                </tr>
            '''
        else:
            html += f'''
                <tr class="hover:bg-primary/5 dark:hover:bg-primary/10 transition-colors duration-150 cursor-pointer"
                    data-type="{file_type}" data-path="{file_path}" data-url-path="{file_url_path}" data-name="{file['name']}">
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                            <span class="material-symbols-outlined mr-3 {icon_class}">{file['icon']}</span>
                            <div class="text-sm font-medium">{file['name']}</div>
                        </div>
                    </td>
                    <td class="hidden px-6 py-4 whitespace-nowrap text-sm text-subtle-light dark:text-subtle-dark md:table-cell">
                        {file['modified']}
                    </td>
                    <td class="hidden px-6 py-4 whitespace-nowrap text-sm text-subtle-light dark:text-subtle-dark lg:table-cell">
                        {file['size']}
                    </td>
                </tr>
            '''
    
    return html


def generate_grid_view_html(files, current_path="wwwroot"):
    """Grid görünümü için HTML oluşturur"""
    html = ""
    
    for file in files:
        file_type = "folder" if file['is_dir'] else "file"
        icon_class = "text-primary" if file['is_dir'] else "text-subtle-light dark:text-subtle-dark"
        
        # Dosya/klasör path'ini oluştur
        file_path = f"{current_path}/{file['name']}"
        # URL path'ini oluştur - BASE_ROOT'u kaldır
        if current_path == BASE_ROOT:
            file_url_path = f"/{file['name']}"
        else:
            file_url_path = f"/{current_path.replace(BASE_ROOT + '/', '')}/{file['name']}"
        
        # Klasörler için tıklanabilir link ekle
        if file['is_dir']:
            html += f'''
                <div class="flex cursor-pointer flex-col items-center gap-2 rounded-lg p-2 text-center transition-colors duration-150 hover:bg-primary/5 dark:hover:bg-primary/10"
                    data-type="{file_type}" data-path="{file_path}" data-url-path="{file_url_path}" data-name="{file['name']}" onclick="window.location.href='{file_url_path}'">
                    <span class="material-symbols-outlined text-5xl {icon_class}">{file['icon']}</span>
                    <span class="text-sm font-medium text-content-light dark:text-content-dark">{file['name']}</span>
                </div>
            '''
        else:
            html += f'''
                <div class="flex cursor-pointer flex-col items-center gap-2 rounded-lg p-2 text-center transition-colors duration-150 hover:bg-primary/5 dark:hover:bg-primary/10"
                    data-type="{file_type}" data-path="{file_path}" data-url-path="{file_url_path}" data-name="{file['name']}">
                    <span class="material-symbols-outlined text-5xl {icon_class}">{file['icon']}</span>
                    <span class="text-sm font-medium text-content-light dark:text-content-dark">{file['name']}</span>
                </div>
            '''
    
    return html


def generate_breadcrumb_html(breadcrumbs):
    """Breadcrumb navigasyon için HTML oluşturur"""
    html = ""
    
    for i, crumb in enumerate(breadcrumbs):
        if i == len(breadcrumbs) - 1:
            # Son eleman (mevcut sayfa)
            html += f'''
                <li aria-current="page" class="font-medium text-content-light dark:text-content-dark">
                    {crumb['name']}
                </li>
            '''
        else:
            # Link elemanları
            crumb_path = f"/{crumb['path']}" if crumb['path'] else "/"
            html += f'''
                <li>
                    <a class="flex items-center gap-1 text-subtle-light dark:text-subtle-dark hover:text-primary dark:hover:text-primary"
                        href="{crumb_path}">
                        <span class="material-symbols-outlined text-base">{crumb['icon']}</span>
                        {crumb['name']}
                    </a>
                </li>
            '''
            
            # Ayırıcı
            if i < len(breadcrumbs) - 1:
                html += '''
                    <li>
                        <span class="text-subtle-light dark:text-subtle-dark">/</span>
                    </li>
                '''
    
    return html


def render_index_html(current_path=None):
    """Ana sayfa HTML'ini dinamik olarak oluşturur"""
    # Varsayılan olarak BASE_ROOT kullan
    if current_path is None:
        current_path = BASE_ROOT
    # Güvenlik kontrolü
    if not is_safe_path(BASE_ROOT, current_path):
        current_path = BASE_ROOT
    
    # Dosya listesini al
    files = list_files_and_folders(current_path)
    breadcrumbs = get_breadcrumb_path(current_path)
    
    # HTML template'i
    html_template = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>File Explorer</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com" rel="preconnect" />
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap"
        rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
    <style type="text/tailwindcss">
        :root {{
            --primary-color: #1173d4;
        }}
        .material-symbols-outlined {{
            font-variation-settings:
                'FILL' 0,
                'wght' 400,
                'GRAD' 0,
                'opsz' 24
        }}
        .context-menu {{
            display: none;
            position: absolute;
            z-index: 10;
        }}
        #list-view-button.active, #grid-view-button.active {{
            background-color: var(--primary-color);
            color: white;
        }}
        #list-view-button.active .material-symbols-outlined, #grid-view-button.active .material-symbols-outlined {{
            color: white;
        }}
    </style>
    <script>
        tailwind.config = {{
            darkMode: "class",
            theme: {{
                extend: {{
                    colors: {{
                        "primary": "var(--primary-color)",
                        "background-light": "#f6f7f8",
                        "background-dark": "#101922",
                        "content-light": "#1a202c",
                        "content-dark": "#e2e8f0",
                        "subtle-light": "#a0aec0",
                        "subtle-dark": "#718096",
                        "border-light": "#e2e8f0",
                        "border-dark": "#2d3748",
                        "surface-light": "#ffffff",
                        "surface-dark": "#1a202c"
                    }},
                    fontFamily: {{
                        "display": ["Inter", "sans-serif"]
                    }},
                    borderRadius: {{
                        "DEFAULT": "0.25rem",
                        "lg": "0.5rem",
                        "xl": "0.75rem",
                        "full": "9999px"
                    }},
                }},
            }},
        }}
    </script>
</head>

<body class="font-display bg-background-light dark:bg-background-dark text-content-light dark:text-content-dark">
    <div class="flex h-screen flex-col">
        <header
            class="flex items-center justify-between border-b border-border-light dark:border-border-dark px-6 py-3">
            <div class="flex items-center gap-3">
                <div class="text-primary">
                    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                            stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                    </svg>
                </div>
                <h1 class="text-lg font-bold">File Explorer</h1>
            </div>
        </header>
        <main class="flex-1 overflow-y-auto p-6 md:p-8 lg:p-10">
            <div class="mx-auto max-w-7xl">
                <div class="mb-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div class="flex flex-1 items-center gap-4">
                        <div class="relative w-full max-w-xs">
                            <span
                                class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-subtle-light dark:text-subtle-dark">search</span>
                            <input
                                class="w-full rounded-md border border-border-light bg-surface-light py-2 pl-10 pr-4 text-sm text-content-light focus:border-primary focus:ring-primary dark:border-border-dark dark:bg-surface-dark dark:text-content-dark dark:focus:border-primary"
                                placeholder="Search files..." type="search" />
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="relative inline-block text-left">
                            <div>
                                <button aria-expanded="true" aria-haspopup="true"
                                    class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-surface-light dark:bg-surface-dark px-3 py-2 text-sm font-semibold text-content-light dark:text-content-dark shadow-sm ring-1 ring-inset ring-border-light dark:ring-border-dark hover:bg-background-light dark:hover:bg-background-dark"
                                    id="menu-button" type="button">
                                    <span
                                        class="material-symbols-outlined -ml-1 h-5 w-5 text-subtle-light dark:text-subtle-dark">sort</span>
                                    Sort
                                    <span
                                        class="material-symbols-outlined -mr-1 h-5 w-5 text-subtle-light dark:text-subtle-dark">arrow_drop_down</span>
                                </button>
                            </div>
                            <div aria-labelledby="menu-button" aria-orientation="vertical"
                                class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-surface-light dark:bg-surface-dark shadow-lg ring-1 ring-border-light dark:ring-border-dark focus:outline-none hidden"
                                role="menu" tabindex="-1">
                                <div class="py-1" role="none">
                                    <a class="text-content-light dark:text-content-dark block px-4 py-2 text-sm hover:bg-background-light dark:hover:bg-background-dark"
                                        href="#" id="menu-item-0" role="menuitem" tabindex="-1">Name</a>
                                    <a class="text-content-light dark:text-content-dark block px-4 py-2 text-sm hover:bg-background-light dark:hover:bg-background-dark"
                                        href="#" id="menu-item-1" role="menuitem" tabindex="-1">Date Modified</a>
                                    <a class="text-content-light dark:text-content-dark block px-4 py-2 text-sm hover:bg-background-light dark:hover:bg-background-dark"
                                        href="#" id="menu-item-2" role="menuitem" tabindex="-1">Size</a>
                                </div>
                            </div>
                        </div>
                        <div
                            class="flex items-center rounded-md bg-surface-light p-0.5 dark:bg-surface-dark ring-1 ring-inset ring-border-light dark:ring-border-dark">
                            <button class="rounded-md p-1.5 text-content-light dark:text-content-dark"
                                id="list-view-button">
                                <span class="material-symbols-outlined text-lg">view_list</span>
                            </button>
                            <button
                                class="rounded-md p-1.5 text-subtle-light dark:text-subtle-dark hover:bg-background-light dark:hover:bg-background-dark"
                                id="grid-view-button">
                                <span class="material-symbols-outlined text-lg">grid_view</span>
                            </button>
                        </div>
                    </div>
                </div>
                <nav aria-label="Breadcrumb" class="mb-4">
                    <ol class="flex items-center gap-1.5 text-sm">
                        {breadcrumb_html}
                    </ol>
                </nav>
                <div class="overflow-hidden rounded-lg border border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark"
                    id="list-view">
                    <table class="w-full text-left">
                        <thead
                            class="border-b border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-subtle-light dark:text-subtle-dark"
                                    scope="col">Name</th>
                                <th class="hidden px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-subtle-light dark:text-subtle-dark md:table-cell"
                                    scope="col">Date Modified</th>
                                <th class="hidden px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-subtle-light dark:text-subtle-dark lg:table-cell"
                                    scope="col">Size</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-border-light dark:divide-border-dark" id="file-list">
                            {file_list_html}
                        </tbody>
                    </table>
                </div>
                <div class="hidden" id="grid-view">
                    <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
                        {grid_view_html}
                    </div>
                </div>
            </div>
        </main>
    </div>
    <div class="context-menu w-48 rounded-md bg-surface-light dark:bg-surface-dark shadow-lg ring-1 ring-border-light dark:ring-border-dark"
        id="context-menu">
        <div class="py-1" id="file-menu">
            <a class="flex items-center gap-3 px-4 py-2 text-sm text-content-light dark:text-content-dark hover:bg-background-light dark:hover:bg-background-dark"
                href="#" data-action="rename">
                <span class="material-symbols-outlined text-base">edit</span>Rename
            </a>
            <a class="flex items-center gap-3 px-4 py-2 text-sm text-content-light dark:text-content-dark hover:bg-background-light dark:hover:bg-background-dark"
                href="#" data-action="delete">
                <span class="material-symbols-outlined text-base">delete</span>Delete
            </a>
            <a class="flex items-center gap-3 px-4 py-2 text-sm text-content-light dark:text-content-dark hover:bg-background-light dark:hover:bg-background-dark"
                href="#" data-action="download">
                <span class="material-symbols-outlined text-base">download</span>Download
            </a>
        </div>
        <div class="py-1" id="folder-menu">
            <a class="flex items-center gap-3 px-4 py-2 text-sm text-content-light dark:text-content-dark hover:bg-background-light dark:hover:bg-background-dark"
                href="#" data-action="rename">
                <span class="material-symbols-outlined text-base">edit</span>Rename
            </a>
            <a class="flex items-center gap-3 px-4 py-2 text-sm text-content-light dark:text-content-dark hover:bg-background-light dark:hover:bg-background-dark"
                href="#" data-action="delete">
                <span class="material-symbols-outlined text-base">delete</span>Delete
            </a>
        </div>
    </div>
    
    <!-- Rename Modal -->
    <div id="rename-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-50">
        <div class="relative w-full max-w-md rounded-lg bg-surface-light dark:bg-surface-dark p-6 shadow-xl">
            <div class="mb-4 flex items-center justify-between">
                <h3 class="text-lg font-semibold text-content-light dark:text-content-dark">Yeniden Adlandır</h3>
                <button id="rename-modal-close" class="text-subtle-light dark:text-subtle-dark hover:text-content-light dark:hover:text-content-dark">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <div class="mb-4">
                <label class="mb-2 block text-sm font-medium text-content-light dark:text-content-dark">Yeni İsim:</label>
                <input type="text" id="rename-input" 
                    class="w-full rounded-md border border-border-light bg-background-light py-2 px-3 text-sm text-content-light focus:border-primary focus:ring-primary dark:border-border-dark dark:bg-background-dark dark:text-content-dark dark:focus:border-primary"
                    placeholder="Dosya adı">
                <p id="rename-error" class="mt-2 hidden text-sm text-red-600 dark:text-red-400"></p>
            </div>
            <div class="flex justify-end gap-2">
                <button id="rename-cancel" 
                    class="rounded-md border border-border-light bg-surface-light px-4 py-2 text-sm font-medium text-content-light hover:bg-background-light dark:border-border-dark dark:bg-surface-dark dark:text-content-dark dark:hover:bg-background-dark">
                    İptal
                </button>
                <button id="rename-confirm" 
                    class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90">
                    Kaydet
                </button>
            </div>
        </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div id="delete-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-50">
        <div class="relative w-full max-w-md rounded-lg bg-surface-light dark:bg-surface-dark p-6 shadow-xl">
            <div class="mb-4 flex items-center justify-between">
                <h3 class="text-lg font-semibold text-content-light dark:text-content-dark">Silme Onayı</h3>
                <button id="delete-modal-close" class="text-subtle-light dark:text-subtle-dark hover:text-content-light dark:hover:text-content-dark">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <div class="mb-6">
                <div class="mb-3 flex items-center gap-3">
                    <span class="material-symbols-outlined text-5xl text-red-600 dark:text-red-400">warning</span>
                    <div>
                        <p class="text-sm text-content-light dark:text-content-dark">
                            <span id="delete-item-name" class="font-semibold"></span> öğesini silmek istediğinize emin misiniz?
                        </p>
                        <p class="mt-2 text-xs text-subtle-light dark:text-subtle-dark">Bu işlem geri alınamaz.</p>
                    </div>
                </div>
            </div>
            <div class="flex justify-end gap-2">
                <button id="delete-cancel" 
                    class="rounded-md border border-border-light bg-surface-light px-4 py-2 text-sm font-medium text-content-light hover:bg-background-light dark:border-border-dark dark:bg-surface-dark dark:text-content-dark dark:hover:bg-background-dark">
                    İptal
                </button>
                <button id="delete-confirm" 
                    class="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700">
                    Sil
                </button>
            </div>
        </div>
    </div>
    
    <!-- Alert Modal -->
    <div id="alert-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-50">
        <div class="relative w-full max-w-md rounded-lg bg-surface-light dark:bg-surface-dark p-6 shadow-xl">
            <div class="mb-4 flex items-center justify-between">
                <h3 id="alert-title" class="text-lg font-semibold text-content-light dark:text-content-dark">Bilgi</h3>
                <button id="alert-close" class="text-subtle-light dark:text-subtle-dark hover:text-content-light dark:hover:text-content-dark">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <div class="mb-6">
                <p id="alert-message" class="text-sm text-content-light dark:text-content-dark"></p>
            </div>
            <div class="flex justify-end">
                <button id="alert-ok" 
                    class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90">
                    Tamam
                </button>
            </div>
        </div>
    </div>
    
    <script>
        const listViewButton = document.getElementById('list-view-button');
        const gridViewButton = document.getElementById('grid-view-button');
        const listView = document.getElementById('list-view');
        const gridView = document.getElementById('grid-view');
        function setActiveButton(button) {{
            // Reset both buttons
            listViewButton.classList.remove('active', 'bg-primary', 'text-white');
            listViewButton.classList.add('text-subtle-light', 'dark:text-subtle-dark');
            gridViewButton.classList.remove('active', 'bg-primary', 'text-white');
            gridViewButton.classList.add('text-subtle-light', 'dark:text-subtle-dark');
            // Set active button
            button.classList.add('active', 'bg-primary', 'text-white');
            button.classList.remove('text-subtle-light', 'dark:text-subtle-dark');
        }}
        // Görünüm tercihini localStorage'dan yükle veya varsayılan olarak 'list' kullan
        const savedView = localStorage.getItem('preferredView') || 'list';
        
        // Görünümü değiştiren fonksiyon
        function switchView(viewType) {{
            if (viewType === 'list') {{
                listView.classList.remove('hidden');
                gridView.classList.add('hidden');
                setActiveButton(listViewButton);
                localStorage.setItem('preferredView', 'list');
            }} else {{
                gridView.classList.remove('hidden');
                listView.classList.add('hidden');
                setActiveButton(gridViewButton);
                localStorage.setItem('preferredView', 'grid');
            }}
        }}
        
        listViewButton.addEventListener('click', () => {{
            switchView('list');
        }});
        gridViewButton.addEventListener('click', () => {{
            switchView('grid');
        }});
        
        // Sayfa yüklendiğinde kaydedilmiş görünüm tercihini uygula
        switchView(savedView);
        
        // Context menu için değişkenler
        const fileList = document.getElementById('file-list');
        const contextMenu = document.getElementById('context-menu');
        const fileMenu = document.getElementById('file-menu');
        const folderMenu = document.getElementById('folder-menu');
        
        // Seçili item'ı saklamak için değişken
        let selectedItem = null;
        
        // Context menu'yu göster ve seçili item'ı sakla
        function showContextMenu(e, item) {{
            e.preventDefault();
            e.stopPropagation();
            
            if (!item || !item.dataset.type) {{
                return;
            }}
            
            selectedItem = item;
            const itemType = item.dataset.type;
            
            if (itemType === 'file') {{
                fileMenu.style.display = 'block';
                folderMenu.style.display = 'none';
            }} else if (itemType === 'folder') {{
                folderMenu.style.display = 'block';
                fileMenu.style.display = 'none';
            }}
            
            contextMenu.style.display = 'block';
            contextMenu.style.left = e.pageX + 'px';
            contextMenu.style.top = e.pageY + 'px';
            
            console.log('Context menu açıldı:', itemType, selectedItem.dataset.name);
        }}
        
        document.addEventListener('click', (e) => {{
            // Context menu içine tıklanmadıysa veya menu item'ına tıklanmadıysa kapat
            if (!contextMenu.contains(e.target)) {{
                contextMenu.style.display = 'none';
                selectedItem = null;
            }}
        }}, true);
        
        // Context menu içinde tıklamaları engelle (menu'yu kapatmamak için)
        contextMenu.addEventListener('click', (e) => {{
            e.stopPropagation();
        }});
        
        // Liste görünümü için context menu
        fileList.addEventListener('contextmenu', (e) => {{
            const targetRow = e.target.closest('tr');
            if (targetRow && targetRow.dataset.type) {{
                showContextMenu(e, targetRow);
            }}
        }});
        
        // Grid görünümü için context menu - event delegation kullan
        gridView.addEventListener('contextmenu', (e) => {{
            const targetItem = e.target.closest('[data-type]');
            if (targetItem && targetItem.dataset.type) {{
                showContextMenu(e, targetItem);
            }}
        }}, true);
        
        // Modal fonksiyonları
        function showModal(modalId) {{
            const modal = document.getElementById(modalId);
            if (modal) {{
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            }}
        }}
        
        function hideModal(modalId) {{
            const modal = document.getElementById(modalId);
            if (modal) {{
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }}
        }}
        
        function showAlert(title, message) {{
            document.getElementById('alert-title').textContent = title;
            document.getElementById('alert-message').textContent = message;
            showModal('alert-modal');
        }}
        
        // Dosya uzantısını al
        function getFileExtension(filename) {{
            const lastDot = filename.lastIndexOf('.');
            if (lastDot === -1 || lastDot === 0 || lastDot === filename.length - 1) {{
                return '';
            }}
            return filename.substring(lastDot);
        }}
        
        // Dosya adını uzantısız al
        function getFileNameWithoutExtension(filename) {{
            const lastDot = filename.lastIndexOf('.');
            if (lastDot === -1 || lastDot === 0) {{
                return filename;
            }}
            return filename.substring(0, lastDot);
        }}
        
        // Rename fonksiyonu
        function renameItem() {{
            if (!selectedItem) {{
                console.error('Rename: selectedItem yok');
                return;
            }}
            
            const oldName = selectedItem.dataset.name;
            const filePath = selectedItem.dataset.path;
            const isFile = selectedItem.dataset.type === 'file';
            
            // Dosya ise uzantıyı al, klasör ise boş
            const extension = isFile ? getFileExtension(oldName) : '';
            const nameWithoutExt = isFile ? getFileNameWithoutExtension(oldName) : oldName;
            
            // Input'u hazırla
            const renameInput = document.getElementById('rename-input');
            const renameError = document.getElementById('rename-error');
            
            renameInput.value = nameWithoutExt;
            renameError.classList.add('hidden');
            renameError.textContent = '';
            
            // Modal'ı göster
            showModal('rename-modal');
            
            // Input'a focus ver
            setTimeout(() => {{
                renameInput.focus();
                renameInput.select();
            }}, 100);
            
            // Enter tuşu ile kaydet
            const handleRenameKeyPress = (e) => {{
                if (e.key === 'Enter') {{
                    e.preventDefault();
                    confirmRename();
                }} else if (e.key === 'Escape') {{
                    e.preventDefault();
                    cancelRename();
                }}
            }};
            
            renameInput.addEventListener('keydown', handleRenameKeyPress);
            
            // Rename confirm fonksiyonu
            window.confirmRename = function() {{
                let newName = renameInput.value.trim();
                
                if (!newName) {{
                    renameError.textContent = 'Dosya adı boş olamaz';
                    renameError.classList.remove('hidden');
                    return;
                }}
                
                // Geçersiz karakter kontrolü
                if (/[<>:"/\\\\|?*]/.test(newName)) {{
                    renameError.textContent = 'Dosya adında geçersiz karakterler var';
                    renameError.classList.remove('hidden');
                    return;
                }}
                
                // Dosya ise uzantıyı ekle
                if (isFile && extension) {{
                    newName = newName + extension;
                }}
                
                if (newName === oldName) {{
                    hideModal('rename-modal');
                    return;
                }}
                
                // Loading durumu
                const confirmBtn = document.getElementById('rename-confirm');
                const originalText = confirmBtn.textContent;
                confirmBtn.disabled = true;
                confirmBtn.textContent = 'Kaydediliyor...';
                
                fetch('/api/rename', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        path: filePath,
                        new_name: newName
                    }})
                }})
                .then(response => response.json())
                .then(data => {{
                    confirmBtn.disabled = false;
                    confirmBtn.textContent = originalText;
                    
                    if (data.success) {{
                        hideModal('rename-modal');
                        showAlert('Başarılı', 'Dosya/klasör başarıyla yeniden adlandırıldı');
                        setTimeout(() => {{
                            window.location.reload();
                        }}, 1000);
                    }} else {{
                        renameError.textContent = data.message || 'Bir hata oluştu';
                        renameError.classList.remove('hidden');
                    }}
                }})
                .catch(error => {{
                    console.error('Hata:', error);
                    confirmBtn.disabled = false;
                    confirmBtn.textContent = originalText;
                    renameError.textContent = 'Bir hata oluştu';
                    renameError.classList.remove('hidden');
                }});
            }};
            
            // Rename cancel fonksiyonu
            window.cancelRename = function() {{
                hideModal('rename-modal');
                renameInput.removeEventListener('keydown', handleRenameKeyPress);
            }};
        }}
        
        // Delete için global değişken
        let itemToDelete = null;
        
        // Delete fonksiyonu
        function deleteItem() {{
            if (!selectedItem) {{
                console.error('Delete: selectedItem yok');
                return;
            }}
            
            // Seçili item'ı sakla
            itemToDelete = selectedItem;
            const fileName = itemToDelete.dataset.name;
            document.getElementById('delete-item-name').textContent = '"' + fileName + '"';
            
            // Modal'ı göster
            showModal('delete-modal');
        }}
        
        // Delete confirm fonksiyonu
        function confirmDelete() {{
            if (!itemToDelete) {{
                console.error('confirmDelete: itemToDelete yok');
                hideModal('delete-modal');
                return;
            }}
            
            const filePath = itemToDelete.dataset.path;
            const fileName = itemToDelete.dataset.name;
            
            console.log('Delete işlemi başlatılıyor:', fileName, filePath);
            
            // Loading durumu
            const confirmBtn = document.getElementById('delete-confirm');
            const originalText = confirmBtn.textContent;
            confirmBtn.disabled = true;
            confirmBtn.textContent = 'Siliniyor...';
            
            fetch('/api/delete?path=' + encodeURIComponent(filePath), {{
                method: 'DELETE'
            }})
            .then(response => {{
                console.log('Delete response:', response.status);
                return response.json();
            }})
            .then(data => {{
                console.log('Delete data:', data);
                confirmBtn.disabled = false;
                confirmBtn.textContent = originalText;
                
                if (data.success) {{
                    hideModal('delete-modal');
                    itemToDelete = null;
                    showAlert('Başarılı', 'Dosya/klasör başarıyla silindi');
                    setTimeout(() => {{
                        window.location.reload();
                    }}, 1000);
                }} else {{
                    hideModal('delete-modal');
                    itemToDelete = null;
                    showAlert('Hata', data.message || 'Bir hata oluştu');
                }}
            }})
            .catch(error => {{
                console.error('Delete hatası:', error);
                confirmBtn.disabled = false;
                confirmBtn.textContent = originalText;
                hideModal('delete-modal');
                itemToDelete = null;
                showAlert('Hata', 'Bir hata oluştu: ' + error.message);
            }});
        }}
        
        // Delete cancel fonksiyonu
        function cancelDelete() {{
            hideModal('delete-modal');
            itemToDelete = null;
        }}
        
        // Download fonksiyonu
        function downloadItem() {{
            if (!selectedItem) {{
                console.error('Download: selectedItem yok');
                return;
            }}
            console.log('Download çağrıldı:', selectedItem.dataset.name);
            
            const filePath = selectedItem.dataset.path;
            
            // Dosya yolunu düzelt (wwwroot/ kısmını kaldır)
            let downloadUrl = filePath.replace('wwwroot/', '');
            // Backslash'leri forward slash'e çevir (Windows path desteği için)
            downloadUrl = downloadUrl.split('\\\\').join('/');
            if (downloadUrl.startsWith('/')) {{
                downloadUrl = downloadUrl.slice(1);
            }}
            
            downloadUrl = '/api/download/' + encodeURIComponent(downloadUrl);
            
            // İndirmeyi başlat
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = selectedItem.dataset.name;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
        
        // Context menu item'larına event listener ekle
        document.querySelectorAll('#file-menu a[data-action], #folder-menu a[data-action]').forEach(menuItem => {{
            menuItem.addEventListener('click', (e) => {{
                e.preventDefault();
                e.stopPropagation();
                
                console.log('Menu item tıklandı:', menuItem.getAttribute('data-action'));
                
                if (!selectedItem) {{
                    console.error('Menu click: selectedItem yok');
                    contextMenu.style.display = 'none';
                    return;
                }}
                
                const action = menuItem.getAttribute('data-action');
                console.log('Action:', action, 'Selected item:', selectedItem.dataset.name);
                
                if (action === 'rename') {{
                    renameItem();
                }} else if (action === 'delete') {{
                    deleteItem();
                }} else if (action === 'download') {{
                    downloadItem();
                }} else {{
                    console.warn('Bilinmeyen action:', action);
                }}
                
                contextMenu.style.display = 'none';
                // selectedItem'ı sıfırlama - modal'lar kullanıyor
            }});
        }});
        
        // Rename modal butonları
        document.getElementById('rename-confirm').addEventListener('click', () => {{
            if (window.confirmRename) {{
                window.confirmRename();
            }}
        }});
        
        document.getElementById('rename-cancel').addEventListener('click', () => {{
            if (window.cancelRename) {{
                window.cancelRename();
            }}
        }});
        
        document.getElementById('rename-modal-close').addEventListener('click', () => {{
            if (window.cancelRename) {{
                window.cancelRename();
            }}
        }});
        
        // Delete modal butonları
        document.getElementById('delete-confirm').addEventListener('click', (e) => {{
            e.preventDefault();
            e.stopPropagation();
            console.log('Delete confirm butonuna tıklandı');
            confirmDelete();
        }});
        
        document.getElementById('delete-cancel').addEventListener('click', (e) => {{
            e.preventDefault();
            e.stopPropagation();
            cancelDelete();
        }});
        
        document.getElementById('delete-modal-close').addEventListener('click', (e) => {{
            e.preventDefault();
            e.stopPropagation();
            cancelDelete();
        }});
        
        // Alert modal butonları
        document.getElementById('alert-ok').addEventListener('click', () => {{
            hideModal('alert-modal');
        }});
        
        document.getElementById('alert-close').addEventListener('click', () => {{
            hideModal('alert-modal');
        }});
        
        // Modal backdrop'a tıklanınca kapat
        document.getElementById('rename-modal').addEventListener('click', (e) => {{
            if (e.target.id === 'rename-modal') {{
                if (window.cancelRename) {{
                    window.cancelRename();
                }}
            }}
        }});
        
        document.getElementById('delete-modal').addEventListener('click', (e) => {{
            if (e.target.id === 'delete-modal') {{
                cancelDelete();
            }}
        }});
        
        document.getElementById('alert-modal').addEventListener('click', (e) => {{
            if (e.target.id === 'alert-modal') {{
                hideModal('alert-modal');
            }}
        }});
    </script>
</body>

</html>'''
    
    # Dinamik içerikleri oluştur
    file_list_html = generate_file_list_html(files, current_path)
    grid_view_html = generate_grid_view_html(files, current_path)
    breadcrumb_html = generate_breadcrumb_html(breadcrumbs)
    
    # Template'i doldur
    final_html = html_template.format(
        file_list_html=file_list_html,
        grid_view_html=grid_view_html,
        breadcrumb_html=breadcrumb_html
    )
    
    return final_html


if __name__ == "__main__":
    # Test için
    html = render_index_html()
    print("HTML oluşturuldu!")
    print(f"Toplam dosya sayısı: {len(list_files_and_folders())}")
