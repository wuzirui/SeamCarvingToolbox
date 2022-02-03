classdef CarveImage
    %CARVEIMAGE 用于作为Seam Carving算法中所处理的图片的封装
    
    properties
        data
        width
        height
        energy_map
    end
    
    methods
        function obj = CarveImage(image)
            %CARVEIMAGE 构造此类的实例
            %   此处显示详细说明
            obj.data = image;
            [obj.height, obj.width] = size(image, 1:2);
            obj.energy_map = obj.computeEnergyMap();
        end

        function obj = removeVerticalSeam(this, seam)
            newImage = uint8(zeros(this.height, this.width - 1, 3));
            for row = 1 : this.height
                newImage(row, 1:(seam(row) - 1), :) = this.data(row, 1:(seam(row) - 1), :);
                newImage(row, seam(row):this.width - 1, :) = this.data(row, (seam(row) + 1):this.width, :);
            end
            obj = CarveImage(newImage);
        end

        function pixel = safeget(obj, row, col)
            row = max(1, min(obj.height, row));
            col = max(1, min(obj.width, col));
            pixel = obj.data(row, col);
        end

        function output = highlightVerticalSeam(obj, seam)
            output = obj.data;
            for row = 1 : obj.height
                output(row, seam(row), :) = [255 0 0];
            end
        end

        function seam = getRandomVerticalSeam(obj)
            seam = unidrnd(obj.width, obj.height, 1);
        end

        function energy = computeEnergyMap(obj)
            kernel = [-1 0 1];
            blur_img = imfilter(obj.data, fspecial('gaussian', 10), 'replicate');
            x_conv = imfilter(blur_img, kernel, 'replicate') .^ 2;
            y_conv = imfilter(blur_img, kernel', 'replicate') .^ 2;
            energy = sum(x_conv, 3) + sum(y_conv, 3);
        end

        function seam = computeVerticalSeam(obj)
            seam = zeros(obj.height, 1);
            lastrow = obj.energy_map(obj.height, :);
%           找最后一行中所有能量值最小的点
            lastvalue = min(lastrow);
            all_available_idx = find(lastrow == lastvalue);
%           随机选择其中一个作为起始点
            lastidx = all_available_idx(unidrnd(size(all_available_idx, 2)));
            seam(obj.height) = lastidx;
            for row = obj.height - 1:-1:1
                available_next = [lastidx - 1, lastidx, lastidx + 1];
                available_next = available_next(available_next > 0);
                available_next = available_next(available_next <= obj.width);
                [~, argmin] = min(obj.energy_map(row, available_next));
                lastidx = available_next(argmin);
                seam(row) = lastidx;
            end
        end

    end
end

