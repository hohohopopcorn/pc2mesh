# taken from https://github.com/mikedh/trimesh/blob/master/examples/offscreen_render.py

import numpy as np
import trimesh


if __name__ == '__main__':
    # print logged messages
    #trimesh.util.attach_to_log()

    # load a mesh
    mesh = trimesh.load('out.obj')

    # get a scene object containing the mesh, this is equivalent to:
    # scene = trimesh.scene.Scene(mesh)
    scene = mesh.scene()

    # a 45 degree homogeneous rotation matrix around
    # the Y axis at the scene centroid
    rotate = trimesh.transformations.rotation_matrix(
        angle=np.radians(30.0),
        direction=[-1, 1, 0],
        point=scene.centroid)

    for i in range(1):
        #trimesh.constants.log.info('Saving image %d', i)

        # rotate the camera view transform
        camera_old, _geometry = scene.graph[scene.camera.name]
        camera_new = np.dot(rotate, camera_old)

        # apply the new transform
        scene.graph[scene.camera.name] = camera_new

        # saving an image requires an opengl context, so if -nw
        # is passed don't save the image
        try:
            # increment the file name
            file_name = 'render.png'
            # save a render of the object as a png
            png = scene.save_image(resolution=[512, 512], visible=True)
            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()

        except BaseException as E:
            print("unable to save image", str(E))