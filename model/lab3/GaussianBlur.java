import java.awt.*;
import java.io.*;
import javax.imageio.*;
import javax.swing.*;
import java.awt.image.BufferedImage;

public class GaussianBlur {
    /**
     * Функция Гаусса от 2 переменных
     * @param x - координата x
     * @param y - координата y
     * @param sigma - стандартное отклонение для x и y
     * @param muX - мат ожидание для x
     * @param muY - мат ожидание для y
     * @return значение функции
     */
    private static double gauss(int x, int y, double sigma, double muX, double muY) {
        return 1 / (2 * Math.PI * Math.pow(sigma, 2)) * Math.exp(-(Math.pow(x-muX, 2) + Math.pow(y-muY, 2)) / (2 * Math.pow(sigma, 2)));
    }

    /**
     * Нормализованное квадратное ядро Гауссовой свертки
     * @param ksize - размер ядра
     * @param sigma - стандартное отклонение для функции Гаусса
     * @param muX - мат ожидание x для функции Гаусса
     * @param muY - мат ожидание y для функции Гаусса
     * @return ядро
     */
    private static double[][] gaussKernel(int ksize, double sigma, double muX, double muY) {
        if (ksize < 0 || ksize % 2 == 0) {
            throw new IllegalArgumentException("Размер ядра должен быть нечетным положительным числом!");
        }
        double[][] kernel = new double[ksize][ksize];
        for (int i = 0; i != ksize; ++i) {
            for (int j = 0; j != ksize; ++j) {
                kernel[i][j] = gauss(i, j, sigma, muX, muY);
            }
        }
        double sum = 0;
        for (int i = 0; i != ksize; ++i) {
            for (int j = 0; j != ksize; ++j) {
                sum += kernel[i][j];
            }
        }
        if (sum != 0) {
            for (int i = 0; i != ksize; ++i) {
                for (int j = 0; j != ksize; ++j) {
                    kernel[i][j] /= sum;
                }
            }
        }
        return kernel;
    }

    /**
     * Квадратное ядро Гауссовой свертки. muY берется равным muX.
     * @param ksize - размер ядра
     * @param sigma - стандартное отклонение для функции Гаусса
     * @param muX - мат ожидание x для функции Гаусса
     * @return ядро
     */
    private static double[][] gaussKernel(int ksize, double sigma, double muX) {
        return gaussKernel(ksize, sigma, muX, muX);
    }

    /**
     * Квадратное ядро Гауссовой свертки. muY и muX берутся равными ksize / 2.  
     * @param ksize - размер ядра
     * @param sigma - стандартное отклонение для функции Гаусса
     * @return ядро
     */
    private static double[][] gaussKernel(int ksize, double sigma) {
        return gaussKernel(ksize, sigma, ksize / 2);
    }

    /**
     * Применяет операцию свертки к каждому внутреннему пикселю изображения
     * @param img - изображение
     * @param kernel - ядро свертки
     * @param ksize - размер ядра свертки
     * @return изображение-результат применения свертки
     */
    private static BufferedImage applyConvolution(BufferedImage img, double[][] kernel, int ksize) {
        int h = img.getHeight(), w = img.getWidth();
        int margin = ksize / 2;
        BufferedImage resultImage = new BufferedImage(w-2*margin, h-2*margin, BufferedImage.TYPE_INT_RGB);
        for (int y = margin; y != h - margin; ++y) {
            for (int x = margin; x != w - margin; ++x) {
                int r = 0, g = 0, b = 0;
                for (int y0 = y - margin; y0 != y + margin + 1; ++y0) {
                    for (int x0 = x - margin; x0 != x + margin + 1; ++x0) {
                        Color pixel = new Color(img.getRGB(x0, y0));
                        r += (int) (pixel.getRed() * kernel[y0-(y-margin)][x0-(x-margin)]);
                        g += (int) (pixel.getGreen() * kernel[y0-(y-margin)][x0-(x-margin)]);
                        b += (int) (pixel.getBlue() * kernel[y0-(y-margin)][x0-(x-margin)]);
                    }
                }
                resultImage.setRGB(x-margin, y-margin, new Color(r, g, b).getRGB());
            }
        }
        return resultImage;
    }

    /**
     * Гауссово размытие изображения
     * @param img - изображение
     * @param ksize - размер ядра свертки
     * @param sigma - степень размытия
     * @return размытое изображение
     */
    private static BufferedImage blurImage(BufferedImage img, int ksize, double sigma) {
        var kernel = gaussKernel(ksize, sigma);
        BufferedImage blurred = applyConvolution(img, kernel, ksize);
        return blurred;
    }
 
    public static void main(String[] args) {
        String imgPath = "/home/egorp/Изображения/druid.jpeg";
        int ksize = 5;
        double sigma = 1.5;

        try {
            BufferedImage img = ImageIO.read(new File(imgPath));
            
            JFrame origFrame = new JFrame("original");
            origFrame.add(new Component() {
                @Override public void paint(Graphics g) {
                    g.drawImage(img, 0, 0, null);
                }
    
                @Override
                public Dimension getPreferredSize() {
                    return new Dimension(img.getWidth(null), img.getHeight(null));
                }
            });
            origFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            origFrame.pack();
            origFrame.setLocation(400, 100);
            origFrame.setVisible(true);


            BufferedImage blur = blurImage(img, ksize, sigma); 
            
            JFrame blurFrame = new JFrame("blurred");
            blurFrame.add(new Component() {
                @Override public void paint(Graphics g) {
                    g.drawImage(blur, 0, 0, null);
                }
    
                @Override
                public Dimension getPreferredSize() {
                    return new Dimension(blur.getWidth(null), blur.getHeight(null));
                }
            });
            blurFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            blurFrame.pack();
            blurFrame.setLocation(900, 100);
            blurFrame.setVisible(true);
            
        } catch (IOException e) {
            System.out.println(
                String.format("Ошибка при чтении файла: %s !", imgPath)
            );
        }
    }
}
