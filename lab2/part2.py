import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

image_raw = imread('brela.jpg')
print(image_raw.shape)

image_sum = image_raw.sum(axis=2)
print(image_sum.shape)
image_gray_scale = image_sum / image_sum.max()

plt.imshow(image_gray_scale, cmap='gray', vmin=0, vmax=1)
plt.colorbar()
plt.title('Brela gray scale', color='white', backgroundcolor='black')
plt.show()

image_flattened = image_gray_scale.reshape(-1, image_gray_scale.shape[1])
pca = PCA()
pca.fit(image_flattened)
cumulative_variance = np.cumsum(pca.explained_variance_ratio_)  # cumulative variance

plt.figure(figsize=(8, 5))  # visualisation of cumulative variance
plt.plot(cumulative_variance, marker='*', color='#B00')
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')
plt.title('Cumulative explained variance & Number of components')
plt.grid(True)
plt.show()

series = plt.figure(figsize=(16, 6), dpi=100)
part = series.subplots(2, 3, sharey=True, sharex=True)

percentage = 35
for i in range(6):
    num_components_i = np.argmax(cumulative_variance >= percentage/100) + 1
    pca_i = PCA(n_components=num_components_i)
    image_reduced = pca_i.fit_transform(image_flattened)
    image_reconstructed = pca_i.inverse_transform(image_reduced)
    image_reconstructed_2d = image_reconstructed.reshape(image_gray_scale.shape)
    percentage += 10

    plot_row = i // 3
    plot_column = i % 3

    part[plot_row, plot_column].imshow(image_reconstructed_2d, cmap='gray')
    part[plot_row, plot_column].set_title(f'Reconstructed image ({percentage}% variance)')

plt.show()
