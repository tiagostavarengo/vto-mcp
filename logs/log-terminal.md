(venv) C:\projects-arenque\vto-arenque\backend>uvicorn main:app --reload
INFO: Will watch for changes in these directories: ['C:\\projects-arenque\\vto-arenque\\backend']
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process [11056] using WatchFiles
INFO: Started server process [2976]
INFO: Waiting for application startup.
INFO: Application startup complete.
Iniciando processo de Virtual Try-On...
Executando detecção de pose com MediaPipe...
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
W0000 00:00:1757531170.170217 9992 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
W0000 00:00:1757531170.196449 9992 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
C:\projects-arenque\vto-arenque\backend\venv\lib\site-packages\google\protobuf\symbol_database.py:55: UserWarning: SymbolDatabase.GetPrototype() is deprecated. Please use message_factory.GetMessageClass() instead. SymbolDatabase.GetPrototype() will be removed soon.
warnings.warn('SymbolDatabase.GetPrototype() is deprecated. Please '
Imagem com pose salva em: debug_images\debug_02_pose_estimation.png
Pontos-chave da pose salvos em: debug_images\debug_02_pose_keypoints.json
Executando remoção de fundo com rembg...
Remoção de fundo concluída.
Iniciando geração de imagem com SwapNet...
Imagens de entrada salvas em: temp_inference
Running warp inference...
Rebuilding warp from C:\projects-arenque\vto-arenque\temp_swapnet\checkpoints\deep_fashion\warp\latest_net_generator.pth
Not overriding: {'reload'}
initialize network with kaiming
initialize network with kaiming
model [WarpModel] was created
loading the model generator from C:\projects-arenque\vto-arenque\temp_swapnet\checkpoints\deep_fashion\warp\latest_net_generator.pth
---------- Networks initialized -------------
[Network generator] Total number of parameters : 137.584 M
[Network discriminator] Total number of parameters : 2.784 M

---

Not overriding: {'reload'}
Creating dataset warp... cloth dir temp_inference\cloth
Extensions: None
body dir temp_inference\body
dataset [WarpDataset] was created
Warping cloth to match body segmentations in temp_inference\body...
100%|████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:06<00:00, 6.81s/img]
Warp results stored in temp_inference\results\warp
Running texture inference...
Rebuilding texture from C:\projects-arenque\vto-arenque\temp_swapnet\checkpoints\deep_fashion\texture\latest_net_generator.pth
Not overriding: {'reload'}
initialize network with kaiming
initialize network with kaiming
C:\projects-arenque\vto-arenque\backend\venv\lib\site-packages\torchvision\models_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
warnings.warn(
C:\projects-arenque\vto-arenque\backend\venv\lib\site-packages\torchvision\models_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=VGG16_Weights.IMAGENET1K_V1`. You can also use `weights=VGG16_Weights.DEFAULT` to get the most up-to-date weights.
warnings.warn(msg)
model [TextureModel] was created
loading the model generator from C:\projects-arenque\vto-arenque\temp_swapnet\checkpoints\deep_fashion\texture\latest_net_generator.pth
---------- Networks initialized -------------
[Network generator] Total number of parameters : 41.900 M
[Network discriminator] Total number of parameters : 2.784 M

---

Not overriding: {'reload'}
Creating dataset texture... dataset [TextureDataset] was created
Texturing cloth segmentations in temp_inference\results\warp...
C:\projects-arenque\vto-arenque\temp_swapnet\datasets\data_utils.py:343: UserWarning: torch.sparse.SparseTensor(indices, values,
shape, \*, device=) is deprecated. Please use torch.sparse_coo_tensor(indices, values, shape, dtype=, device=). (Triggered internally at C:\actions-runner_work\pytorch\pytorch\pytorch\torch\csrc\utils\tensor_new.cpp:655.)
return torch.sparse.FloatTensor(indices, values, torch.Size(shape)).to_dense()
Textured results stored in temp_inference\results\texture
Shape of fakes_tensor: torch.Size([1, 3, 128, 128])
Debug fakes_tensor saved to debug_images\debug_fakes_tensor.png
Diretório temporário removido: temp_inference
Processo de Virtual Try-On concluído.
INFO: 127.0.0.1:60996 - "POST /api/tryon HTTP/1.1" 200 OK
