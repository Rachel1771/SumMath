clc
% p1outdata�Ǿ����˹�����ĸ���1������
% ��һ������ҵ����
% �ڶ�����������
% ������������˰��
% �����д���Ʊ״̬��1Ϊ��Ч��Ʊ��0Ϊ���Ϸ�Ʊ
[line,column]=size(p1outdata);
result=zeros(123,7);
for i=1:123
    result(i,1)=i;
end
for i=1:123
    count=0;% �ܼ�����
    effective_count=0;% ��Ч��Ʊ������
    negative_count=0;% ������Ʊ������
    output_sum=0;% �����ܶ�
    tax_sum=0;% ˰�ܶ�
    max_output=0;% �������
    max_tax=0;% ���˰��
    for j=1:line
        if p1outdata(j,1) == i % ��Ӧ��˾
            count=count+1; % ���ܷ�Ʊ��
            if p1outdata(j,4) == 1 % �������Ч��Ʊ
                effective_count=effective_count+1; % ����Ч��Ʊ��
                if p1outdata(j,2)<0 % ����Ǹ�����Ʊ
                    negative_count=negative_count+1; % ������Ʊ��
                end
            	output_sum=output_sum+p1outdata(j,2);% ��������ܶ�
                tax_sum=tax_sum+p1outdata(j,3);% �������˰�ܶ�
                % ���������
                if p1outdata(j,2)>max_output
                    max_output=p1outdata(j,2);
                end
                % ���������˰��
                if p1outdata(j,3)>max_tax
                    max_tax=p1outdata(j,3);
                end
            end
        elseif p1outdata(j,1)>i
            break;
        end
    end
    result(i,2)=effective_count/count; % ��Ч��
    result(i,3)=negative_count/count;% ������
    result(i,4)=output_sum;
    result(i,5)=tax_sum;
    result(i,6)=max_output;
    result(i,7)=max_tax;
end
