import os
import mimetypes
from datetime import datetime
from pathlib import Path


BASE_ROOT = "wwwroot/data-2"
BASE_ROOT_PREFIX = f"{BASE_ROOT}/"


def get_file_info(file_path):
    """Dosya bilgilerini alır"""
    stat = file_path.stat()
    size = stat.st_size
    
    # Dosya boyutunu okunabilir formata çevir
    if size < 1024:
        size_str = f"{size} B"
    elif size < 1024 * 1024:
        size_str = f"{size / 1024:.1f} KB"
    elif size < 1024 * 1024 * 1024:
        size_str = f"{size / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    return {
        'name': file_path.name,
        'size': size_str,
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
        'is_dir': file_path.is_dir(),
        'extension': file_path.suffix.lower() if not file_path.is_dir() else ''
    }


def get_file_icon(file_info):
    """Dosya türüne göre ikon belirler"""
    if file_info['is_dir']:
        return 'folder'
    
    extension = file_info['extension']
    
    # Dosya türüne göre ikonlar
    icon_map = {
        '.pdf': 'picture_as_pdf',
        '.doc': 'description',
        '.docx': 'description',
        '.txt': 'description',
        '.rtf': 'description',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.png': 'image',
        '.gif': 'image',
        '.svg': 'image',
        '.mp4': 'movie',
        '.avi': 'movie',
        '.mov': 'movie',
        '.mp3': 'audio_file',
        '.wav': 'audio_file',
        '.zip': 'folder_zip',
        '.rar': 'folder_zip',
        '.7z': 'folder_zip',
        '.xlsx': 'table_chart',
        '.xls': 'table_chart',
        '.csv': 'table_chart',
        '.ppt': 'slideshow',
        '.pptx': 'slideshow'
    }
    
    return icon_map.get(extension, 'description')


def list_files_and_folders(root_path=BASE_ROOT):
    """Belirtilen klasördeki dosya ve klasörleri listeler"""
    try:
        root = Path(root_path)
        
        if not root.exists():
            print(f"Klasör bulunamadı: {root_path}")
            return []
        
        items = []
        
        # Önce klasörleri, sonra dosyaları ekle
        for item in sorted(root.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            file_info = get_file_info(item)
            file_info['icon'] = get_file_icon(file_info)
            items.append(file_info)
        
        print(f"Dosya listesi okundu: {root_path} - {len(items)} öğe")
        return items
    
    except Exception as e:
        print(f"Dosya listesi alınırken hata: {e}")
        return []


def get_current_path_from_url(url_path):
    """URL path'inden gerçek dosya yolunu oluşturur"""
    if not url_path or url_path == '/':
        return BASE_ROOT
    
    # URL path'ini temizle ve kök klasör ile birleştir
    clean_path = url_path.strip('/')
    if clean_path.startswith(BASE_ROOT_PREFIX):
        return clean_path
    else:
        return f"{BASE_ROOT}/{clean_path}"


def is_safe_path(base_path, target_path):
    """Güvenli yol kontrolü - directory traversal saldırılarını önler"""
    try:
        base = Path(base_path).resolve()
        target = Path(target_path).resolve()
        
        # Target path'in base path içinde olup olmadığını kontrol et
        return str(target).startswith(str(base))
    except:
        return False


def get_breadcrumb_path(current_path=BASE_ROOT):
    """Breadcrumb navigasyon için yol oluşturur"""
    path_parts = Path(current_path).parts
    breadcrumbs = []
    
    # Ana dizin
    breadcrumbs.append({
        'name': 'Home',
        'path': '',
        'icon': 'home'
    })
    
    # Alt dizinler
    current_breadcrumb_path = ""
    for part in path_parts:
        if part == BASE_ROOT:
            continue
        current_breadcrumb_path += f"/{part}" if current_breadcrumb_path else part
        breadcrumbs.append({
            'name': part.replace('_', ' ').title(),
            'path': current_breadcrumb_path,
            'icon': 'folder'
        })
    
    return breadcrumbs


def rename_file_or_folder(old_path, new_name):
    """Dosya veya klasörü yeniden adlandırır"""
    try:
        old_file_path = Path(old_path)
        
        if not old_file_path.exists():
            return {'success': False, 'message': 'Dosya veya klasör bulunamadı'}
        
        # Güvenlik kontrolü
        if not is_safe_path(BASE_ROOT, str(old_file_path)):
            return {'success': False, 'message': 'Güvenlik hatası: Geçersiz yol'}
        
        # Yeni adın güvenli olup olmadığını kontrol et
        if not new_name or '/' in new_name or '\\' in new_name:
            return {'success': False, 'message': 'Geçersiz dosya adı'}
        
        # Yeni yol
        new_file_path = old_file_path.parent / new_name
        
        # Hedef yolun güvenli olup olmadığını kontrol et
        if not is_safe_path(BASE_ROOT, str(new_file_path)):
            return {'success': False, 'message': 'Güvenlik hatası: Geçersiz hedef yol'}
        
        # Hedef dosya/klasör zaten varsa
        if new_file_path.exists():
            return {'success': False, 'message': 'Bu isimde bir dosya veya klasör zaten mevcut'}
        
        # Yeniden adlandır
        old_file_path.rename(new_file_path)
        
        return {'success': True, 'message': 'Dosya/klasör başarıyla yeniden adlandırıldı'}
    
    except Exception as e:
        return {'success': False, 'message': f'Hata: {str(e)}'}


def delete_file_or_folder(file_path):
    """Dosya veya klasörü siler"""
    try:
        path = Path(file_path)
        
        if not path.exists():
            return {'success': False, 'message': 'Dosya veya klasör bulunamadı'}
        
        # Güvenlik kontrolü
        if not is_safe_path(BASE_ROOT, str(path)):
            return {'success': False, 'message': 'Güvenlik hatası: Geçersiz yol'}
        
        # Kök klasörün kendisini silmeyi engelle
        if str(path.resolve()) == str(Path(BASE_ROOT).resolve()):
            return {'success': False, 'message': 'Ana klasör silinemez'}
        
        # Klasör ise içindeki tüm dosyaları sil
        if path.is_dir():
            import shutil
            shutil.rmtree(path)
        else:
            path.unlink()
        
        return {'success': True, 'message': 'Dosya/klasör başarıyla silindi'}
    
    except Exception as e:
        return {'success': False, 'message': f'Hata: {str(e)}'}


def get_file_path_for_download(url_path, current_directory=BASE_ROOT):
    """Download için dosya yolunu oluşturur ve güvenlik kontrolü yapar"""
    try:
        # URL path'inden gerçek dosya yolunu al
        if url_path.startswith(f'/{BASE_ROOT_PREFIX}'):
            file_path = Path(url_path[1:])  # Baştan / karakterini kaldır
        elif url_path.startswith('/'):
            # Mevcut klasör içindeki dosya
            clean_path = url_path.strip('/')
            file_path = Path(current_directory) / clean_path
        else:
            file_path = Path(current_directory) / url_path
        
        # Güvenlik kontrolü
        if not is_safe_path(BASE_ROOT, str(file_path.resolve())):
            return None
        
        if not file_path.exists() or file_path.is_dir():
            return None
        
        return file_path
    
    except Exception as e:
        print(f"Download path oluşturulurken hata: {e}")
        return None


if __name__ == "__main__":
    # Test için
    files = list_files_and_folders()
    print("Dosya listesi:")
    for file in files:
        print(f"- {file['name']} ({'Klasör' if file['is_dir'] else 'Dosya'}) - {file['size']} - {file['modified']}")
    
    print("\nBreadcrumb:")
    breadcrumbs = get_breadcrumb_path()
    for crumb in breadcrumbs:
        print(f"- {crumb['name']}")
