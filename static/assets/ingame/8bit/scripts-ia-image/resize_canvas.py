from krita import Krita, InfoObject
import os

def resize_canvas_and_export():
    app = Krita.instance()
    documents = app.documents()
    EXPORT_SUFFIX = "resized_"

    if not documents:
        print("Aucune image n'est ouverte.")
        return

    count = 0
    for doc in documents:
        old_w = doc.width()
        old_h = doc.height()
        
        # 1. Calcul des nouvelles dimensions du tableau
        new_w = 32 if old_w == 30 else (16 if old_w == 18 else (8 if old_w == 10 else old_w))
        new_h = 32 if old_h == 30 else (16 if old_h == 18 else (8 if old_h == 10 else old_h))
        
        # 2. On procède si une dimension change
        if new_w != old_w or new_h != old_h:
            # Calcul pour centrer l'image
            offset_x = (new_w - old_w) // 2
            offset_y = (new_h - old_h) // 2
            
            # Redimensionnement du canevas (tableau)
            doc.resizeImage(-offset_x, -offset_y, new_w, new_h)
            
            # 3. Système d'exportation
            full_path = doc.fileName()
            if full_path:
                base_path = os.path.dirname(full_path)
                base_name = os.path.splitext(os.path.basename(full_path))[0]
                
                # Création du nom de fichier (ex: resized_monImage.png)
                export_path = os.path.join(
                    base_path,
                    f"{EXPORT_SUFFIX}{base_name}.png"
                )

                # Export PNG
                doc.exportImage(export_path, InfoObject())
                print(f"[{doc.name()}] Redimensionné en {new_w}x{new_h} et exporté.")
                count += 1
            else:
                print(f"[{doc.name()}] Modifié mais non exporté (fichier non enregistré sur le disque).")

    # Notification dans Krita
    if app.activeWindow() and app.activeWindow().activeView():
        app.activeWindow().activeView().showFloatingMessage(
            f"{count} image(s) traitées et exportées !", 
            None, 3000, 1
        )

resize_canvas_and_export()