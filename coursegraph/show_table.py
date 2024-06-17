import pandas as pd
import strictyaml as syaml
import os
import sys
import platform
import matplotlib.pyplot as plt
from fontutil import get_system_font  # 폰트 관련 함수를 외부 모듈에서 가져옵니다.
from matplotlib import font_manager, rc
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class ShowTable:
    def __init__(self, image_mode, input_filepath, output_filename, width=None, height=None):
        self.font_path = get_system_font()[0]['file']  # 외부 모듈의 함수를 직접 사용하여 폰트 경로 초기화
        self.filename = input_filepath
        self.output_filename = output_filename
        self.image_mode = image_mode
        self.width = width or 20  # 기본 너비 설정
        self.height = height or 10  # 기본 높이 설정

    def read_subjects(self):
        """
        YAML 파일로부터 데이터를 읽고 파싱합니다.
        파일을 UTF-8로 읽고 Yaml 데이터로 파싱합니다.
        
        Returns:
            dict: 파싱된 데이터
            None: 파일을 찾을 수 없거나 오류가 발생한 경우
        """
        try:
            with open(self.filename, 'r', encoding='UTF8') as file:
                yaml_data = file.read()
                data = syaml.load(yaml_data).data
                return data
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            return None
        except Exception as e:
            print("파일을 읽는 중 오류가 발생했습니다:", e)
            return None

    def make_data(self, data, width, height):
        """
        데이터로부터 테이블을 생성하거나 이미지를 저장합니다.
        """
        font_name = font_manager.FontProperties(fname=self.font_path).get_name()
        rc('font', family=font_name)
        if '과목' in data:
            df = pd.DataFrame(data['과목'])
            df.fillna('', inplace=True)
            df = df.applymap(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
            fig, ax = plt.subplots(figsize=(width, height), dpi=100)
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.2] * len(df.columns))
            ax.set_title('과목 표')
            plt.tight_layout()
            if self.image_mode:
                if self.output_filename:
                    plt.savefig(self.output_filename)
            else:
                plt.show()
        else:
            print("데이터에 '과목' 정보가 없습니다.")

    def process_data(self):
        """
        데이터 처리를 진행하고, 결과를 이미지나 표 형태로 생성합니다.
        """
        subjects = self.read_subjects()
        if subjects:
            self.make_data(subjects, self.width, self.height)

if __name__ == "__main__":
    # 인스턴스 생성 및 데이터 처리
    data_processor = ShowTable(image_mode=True, input_filepath="input.yaml", output_filename="output.png", width=10, height=6)
    data_processor.process_data()
