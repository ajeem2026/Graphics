        # A blue table

        # Made from several boxes SO USE BOXGEO
        # Use a Group object to organize the table as a single object in the world.

        table = Group()
        tableGeo = BoxGeometry(width=4, height=0.2, depth=2)
        # bleu color table
        tableMat = SurfaceMaterial(
            {"useVertexColors": False, "baseColor": [0, 0, 1]})
        tableMesh = MovingMesh(tableGeo, tableMat)

        tableMesh.setPosition([0, 1.5, 0])
        table.add(tableMesh)