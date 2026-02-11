from krita import Krita, InfoObject
import os

def resize_opened_images():
    app = Krita.instance()
    documents = app.documents()
    EXPORT_SUFFIX = "300x300_"

    if not documents:
        print("Aucune image n'est ouverte.")
        return

    count = 0
    for doc in documents:
        # On récupère la résolution actuelle pour ne pas la changer
        x_res = int(doc.xRes())
        y_res = int(doc.yRes())
        
        # --- LA CORRECTION EST ICI ---
        # On multiplie la largeur/hauteur (15px) par 20 pour arriver à 300px
        target_width = doc.width() * 20
        target_height = doc.height() * 20
        
        doc.scaleImage(target_width, target_height, x_res, y_res, "Box")
        count += 1
        
        # --- Exportation ---
        full_path = doc.fileName()
        if full_path:
            base_path = os.path.dirname(full_path)
            base_name = os.path.splitext(os.path.basename(full_path))[0]
            
            export_path = os.path.join(
                base_path,
                EXPORT_SUFFIX + base_name + ".png"
            )

            doc.exportImage(export_path, InfoObject())
            print(f"Exporté : {export_path} ({target_width}x{target_height})")
        
    if app.activeWindow():
        app.activeWindow().activeView().showFloatingMessage(
            f"{count} image(s) en 300x300 exportées !", 
            None, 3000, 1
        )

resize_opened_images()