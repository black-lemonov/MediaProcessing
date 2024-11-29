import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class CannyEdgeDetection {

    public static BufferedImage applyGaussianBlur(BufferedImage image) {
        float[][] kernel = {
                {1/16f, 2/16f, 1/16f},
                {2/16f, 4/16f, 2/16f},
                {1/16f, 2/16f, 1/16f}
        };
        return applyKernel(image, kernel);
    }

    public static BufferedImage applyKernel(BufferedImage image, float[][] kernel) {
        int width = image.getWidth();
        int height = image.getHeight();
        BufferedImage output = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        int kernelHeight = kernel.length;
        int kernelWidth = kernel[0].length;
        int kernelCenterX = kernelWidth / 2;
        int kernelCenterY = kernelHeight / 2;

        for (int y = kernelCenterY; y < height - kernelCenterY; y++) {
            for (int x = kernelCenterX; x < width - kernelCenterX; x++) {
                float sum = 0;
                for (int ky = 0; ky < kernelHeight; ky++) {
                    for (int kx = 0; kx < kernelWidth; kx++) {
                        int pixel = image.getRGB(x + kx - kernelCenterX, y + ky - kernelCenterY);
                        Color color = new Color(pixel);
                        float gray = (color.getRed() + color.getGreen() + color.getBlue()) / 3f;
                        sum += gray * kernel[ky][kx];
                    }
                }
                int gray = Math.min(Math.max((int) sum, 0), 255);
                Color newColor = new Color(gray, gray, gray);
                output.setRGB(x, y, newColor.getRGB());
            }
        }

        return output;
    }

    public static float[][] computeGradient(BufferedImage image) {
        int width = image.getWidth();
        int height = image.getHeight();
        float[][] gradientLength = new float[height][width];
        float[][] gradientDirection = new float[height][width];

        int[][] sobelX = {
                {-1, 0, 1},
                {-2, 0, 2},
                {-1, 0, 1}
        };
        int[][] sobelY = {
                {-1, -2, -1},
                {0, 0, 0},
                {1, 2, 1}
        };

        for (int y = 1; y < height - 1; y++) {
            for (int x = 1; x < width - 1; x++) {
                float gx = 0, gy = 0;
                for (int ky = -1; ky <= 1; ky++) {
                    for (int kx = -1; kx <= 1; kx++) {
                        int pixel = image.getRGB(x + kx, y + ky);
                        Color color = new Color(pixel);
                        float gray = (color.getRed() + color.getGreen() + color.getBlue()) / 3f;
                        gx += gray * sobelX[ky + 1][kx + 1];
                        gy += gray * sobelY[ky + 1][kx + 1];
                    }
                }
                gradientLength[y][x] = (float) Math.sqrt(gx * gx + gy * gy);
                gradientDirection[y][x] = (float) Math.atan2(gy, gx) * (180 / (float) Math.PI);
            }
        }

        return gradientLength;
    }

    public static BufferedImage nonMaxSuppression(BufferedImage image, float[][] gradientLength, float[][] gradientDirection) {
        int width = image.getWidth();
        int height = image.getHeight();
        BufferedImage output = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);

        for (int y = 1; y < height - 1; y++) {
            for (int x = 1; x < width - 1; x++) {
                float direction = gradientDirection[y][x];
                float magnitude = gradientLength[y][x];
                
                if ((direction < 22.5 && direction >= -22.5) || (direction >= 157.5 || direction < -157.5)) {
                    // горизонтальные градиенты
                    if (magnitude < gradientLength[y][x - 1] || magnitude < gradientLength[y][x + 1]) {
                        magnitude = 0;
                    }
                } else if (direction >= 22.5 && direction < 67.5) {
                    // угол 45 градусов
                    if (magnitude < gradientLength[y - 1][x + 1] || magnitude < gradientLength[y + 1][x - 1]) {
                        magnitude = 0;
                    }
                } else if (direction >= 67.5 && direction < 112.5) {
                    // вертикальные градиенты
                    if (magnitude < gradientLength[y - 1][x] || magnitude < gradientLength[y + 1][x]) {
                        magnitude = 0;
                    }
                } else if (direction >= 112.5 && direction < 157.5) {
                    // угол 135 градусов
                    if (magnitude < gradientLength[y - 1][x - 1] || magnitude < gradientLength[y + 1][x + 1]) {
                        magnitude = 0;
                    }
                }

                int gray = Math.min(Math.max((int) magnitude, 0), 255);
                Color newColor = new Color(gray, gray, gray);
                output.setRGB(x, y, newColor.getRGB());
            }
        }

        return output;
    }

    public static BufferedImage doubleThreshold(BufferedImage image, float lowThreshold, float highThreshold) {
        int width = image.getWidth();
        int height = image.getHeight();
        BufferedImage output = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int pixel = image.getRGB(x, y);
                Color color = new Color(pixel);
                int gray = color.getRed();
                if (gray >= highThreshold) {
                    output.setRGB(x, y, Color.WHITE.getRGB());
                    continue;
                } else if (gray >= lowThreshold) {
                    output.setRGB(x, y, Color.GRAY.getRGB());
                } else {
                    output.setRGB(x, y, Color.BLACK.getRGB());
                }
            }
        }

        return output;
    }

    public static void showImage(BufferedImage image) {
        JFrame frame = new JFrame("Canny Edge Detection");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(image.getWidth(), image.getHeight());
        JLabel label = new JLabel(new ImageIcon(image));
        frame.add(label);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        try {
            BufferedImage image = javax.imageio.ImageIO.read(new java.io.File("/home/egorp/Изображения/shisui.jpg"));

            BufferedImage blurredImage = applyGaussianBlur(image);
            showImage(blurredImage);
            float[][] gradientLength = computeGradient(blurredImage);
            BufferedImage suppressedImage = nonMaxSuppression(blurredImage, gradientLength, gradientLength);
            showImage(suppressedImage);
            BufferedImage finalImage = doubleThreshold(suppressedImage, 50, 150);

            showImage(finalImage);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
