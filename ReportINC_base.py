import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from mpl_toolkits.mplot3d import Axes3D
from datetime import date
# REPORTLAB
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter, A4
import os
import sys
#test
import traceback
try:
        def logo_choose(self):
                index = self.comboBox.currentIndex()
                logo_cb = index
                return logo_cb


        def generate_report(self):
                # Importing raw data
                survey_in_path = self.lineEdit_8.text()
                survey_in = pd.read_csv(survey_in_path, skiprows = [0, 2])
                #survey_in = survey_in.drop(["Unnamed: 26"], axis = 1)

                survey_out_path = self.lineEdit_9.text()
                survey_out = pd.read_csv(survey_out_path, skiprows = [0, 2])
                #survey_out = survey_out.drop(["Unnamed: 26"], axis = 1)

                # Creating Lists
                survey1 = survey_in.drop(survey_in.index[1:-1])
                survey1 = survey1[["Dip", "Azimuth", "Easting", "Northing", "Elevation"]]
                survey1.index=(['Start of Survey','End of Survey'])
                survey1.reset_index(level=0, inplace=True)
                s1_lol = round(survey1, 2).T.reset_index().values.T.tolist()

                survey2 = survey_out.drop(survey_out.index[1:-1])
                survey2 = survey2[["Dip", "Azimuth", "Easting", "Northing", "Elevation"]]
                survey2.index=(['Start of Survey','End of Survey'])
                survey2.reset_index(level=0, inplace=True)
                s2_lol = round(survey2, 2).T.reset_index().values.T.tolist()

                depth = survey_in["Station"].iloc[-1] - survey_in["Station"].iloc[0]

                #Inputs
                project_id = str(self.lineEdit_17.text())
                bh_id = str(self.lineEdit.text())
                project_loc = str(self.lineEdit_2.text())
                country = "Azerbaijan"
                client = str(self.lineEdit_3.text())
                surveyed_by = str(self.lineEdit_4.text())
                report_by = str(self.lineEdit_5.text())
                temp_survey_date = self.dateEdit.date()
                survey_date = str(temp_survey_date.toPyDate())
                drill_dia = str(self.lineEdit_10.text()) + " mm"
                survey_run = str(self.lineEdit_11.text())
                angular_unit = str(self.lineEdit_12.text())
                linear_unit = str(self.lineEdit_13.text())

                #Survey parameteres
                station_inter = survey_in["Station"].iloc[1] - survey_in["Station"].iloc[0]
                num_stations = len(survey_in["Station"])
                survey_start = survey_in["Station"].iloc[0]
                survey_end = survey_in["Station"].iloc[-1]

                #Today's date
                today = str(date.today().strftime("%d %b %Y"))

                #Calculating misclosure
                end_east_diff = round(survey_out["Easting"].iloc[-1]-survey_in["Easting"].iloc[-1], 2)
                end_nort_diff = round(survey_out["Northing"].iloc[-1]-survey_in["Northing"].iloc[-1], 2)
                end_elev_diff = round(survey_out["Elevation"].iloc[-1]-survey_in["Elevation"].iloc[-1], 2)
                misclosure = round(np.sqrt(end_east_diff**2 + end_nort_diff**2 + end_elev_diff**2), 2)

                # Misclosure QC

                def misclosure_qc(misc, depth1):
                    global qc
                    if misc <= depth1 * 1/100:
                        qc = "Passed"
                    else:
                        qc = "Failed"
                misclosure_qc(misclosure, depth)


                end_dip_diff = round(survey_in["Dip"].iloc[-1] - survey_out["Dip"].iloc[-1], 2)
                end_azimuth_diff = round(survey_in["Azimuth"].iloc[-1] - survey_out["Azimuth"].iloc[-1], 2)
                end_east_diff = round(survey_in["Easting"].iloc[-1] - survey_out["Easting"].iloc[-1], 2)
                end_north_diff = round(survey_in["Northing"].iloc[-1] - survey_out["Northing"].iloc[-1], 2)
                end_elev_diff = round(survey_in["Elevation"].iloc[-1] - survey_out["Elevation"].iloc[-1], 2)

                #Lists for table
                end_of_surv_diff = [["Dip", "Azimuth", "Easting", "Northing", "Elevation"],
                                    [end_dip_diff, end_azimuth_diff, end_east_diff, end_north_diff, end_elev_diff]]

                end_of_surv_misc = [["Depth", "Misclosure", "Misclosure %", "Quality"],
                                    [depth, misclosure, round(misclosure / depth * 100, 2), qc]]

                #Misclosure plot
                misclosure_line = np.linspace(0, misclosure, 50)
                misclosure_max_line = np.linspace(0, survey_out["Station"].iloc[-1]/100, 50)
                depth_line = np.linspace(0, survey_out["Station"].iloc[-1], 50)

                fig1, ax1 = plt.subplots(figsize=(6, 3))
                ax1.plot(depth_line, misclosure_line, color = "orange", label = "Misclosure between surveys")
                ax1.plot(depth_line, misclosure_max_line, color = "purple", label = "Maximum allowed misclosure")
                ax1.set_xlabel("Depth (m)", size = 14)
                ax1.set_ylabel("Meter", size = 14)
                ax1.legend(loc = "best")
                plt.grid(True)
                ax1.set_title("Misclosure", size=14)


                # Borehole path plot

                fig2 = plt.figure(figsize=(7.5, 7.5))
                ax2 = plt.axes(projection='3d')

                # Data for three-dimensional scattered points
                xdata_in = survey_in["Easting"]
                ydata_in = survey_in["Northing"]
                zdata_in = survey_in["Elevation"]

                xdata_out = survey_out["Easting"]
                ydata_out = survey_out["Northing"]
                zdata_out = survey_out["Elevation"]

                ax2.scatter3D(xdata_in, ydata_in, zdata_in, c="orange")
                ax2.plot(xdata_in, ydata_in, zdata_in, c="orange", label="Survey1")
                ax2.scatter3D(xdata_out, ydata_out, zdata_out, c="purple")
                ax2.plot(xdata_out, ydata_out, zdata_out, c="purple", label ="Survey2")
                plt.legend(loc="best")

                x_ticks = np.linspace(xdata_in.min(), xdata_in.max(), 5)
                y_ticks = np.linspace(ydata_in.min(), ydata_in.max(), 5)
                z_ticks = np.linspace(zdata_in.min(), zdata_in.max(), 5)
                plt.tight_layout()
                ax2.set_xlabel('X', size = 14, labelpad=3)
                ax2.set_ylabel('Y', size = 14, labelpad=15)
                ax2.set_zlabel('Z', size = 14, labelpad=10)

                ax2.get_xaxis().get_major_formatter().set_useOffset(False)
                ax2.get_yaxis().get_major_formatter().set_useOffset(False)

                ax2.set_title("Borehole Path", size = 14, pad=20)

                #  DIP PLOT
                fig15, ax15 = plt.subplots(figsize=(7, 4))
                ax15.plot(survey_in["Station"], survey_in["Dip"], color = "orange", label = "Survey 1")
                ax15.plot(survey_out["Station"], survey_out["Dip"], color = "purple", label = "Survey 2")
                ax15.set_xlabel("Depth (m)", size = 14)
                ax15.set_ylabel("Dip", size = 14)
                ax15.legend(loc = "best")
                ax15.grid(True)
                ax15.set_title("Dip", size=14)

                # AZIMUTH PLOT

                fig3, ax3 = plt.subplots(figsize=(7, 4))
                ax3.plot(survey_in["Station"], survey_in["Azimuth"], color = "orange", label = "Survey 1")
                ax3.plot(survey_out["Station"], survey_out["Azimuth"], color = "purple", label = "Survey 2")
                ax3.set_xlabel("Depth (m)", size = 14)
                ax3.set_ylabel("Azimuth", size = 14)
                ax3.legend(loc = "best")
                ax3.grid(True)
                ax3.set_title("Azimuth", size=14)

                # EASTING PLOT

                fig4, ax4 = plt.subplots(figsize=(6, 2.5))
                ax4.plot(survey_in["Station"], survey_in["Easting"], color = "orange", label = "Survey 1")
                ax4.plot(survey_out["Station"], survey_out["Easting"], color = "purple", label = "Survey 2")
                ax4.set_xlabel("Depth (m)", size = 14)
                ax4.set_ylabel("Easting", size = 14)
                ax4.legend(loc = "best")
                ax4.grid(True)
                ax4.get_yaxis().get_major_formatter().set_useOffset(False)
                ax4.set_title("Easting", size=14)


                # NORTHING PLOT

                fig5, ax5 = plt.subplots(figsize=(6, 2.5))
                ax5.plot(survey_in["Station"], survey_in["Northing"], color = "orange", label = "Survey 1")
                ax5.plot(survey_out["Station"], survey_out["Northing"], color = "purple", label = "Survey 2")
                ax5.set_xlabel("Depth (m)", size = 14)
                ax5.set_ylabel("Northing", size = 14)
                ax5.legend(loc = "best")
                ax5.grid(True)
                ax5.get_yaxis().get_major_formatter().set_useOffset(False)
                ax5.set_title("Northing", size=14)


                # ELEVATION PLOT

                fig6, ax6 = plt.subplots(figsize=(6, 2.5))
                ax6.plot(survey_in["Station"], survey_in["Elevation"], color = "orange", label = "Survey 1")
                ax6.plot(survey_out["Station"], survey_out["Elevation"], color = "purple", label = "Survey 2")
                ax6.set_xlabel("Depth (m)", size = 14)
                ax6.set_ylabel("Elevation", size = 14)
                ax6.legend(loc = "best")
                ax6.grid(True)
                ax6.get_yaxis().get_major_formatter().set_useOffset(False)
                ax6.set_title("Elevation", size=14)


                # POSTIONAL COMPARISON

                fig7, ax7 = plt.subplots(figsize=(6.5, 3.5))
                ax7.plot(survey_in["Easting"], survey_in["Northing"], color = "orange", label = "Survey 1")
                ax7.plot(survey_out["Easting"], survey_out["Northing"], color = "purple", label = "Survey 2")
                ax7.set_xlabel("Easting", size = 14)
                ax7.set_ylabel("Northing", size = 14)
                ax7.legend(loc = "best")
                plt.xticks(rotation=40)
                plt.yticks(rotation=40)
                ax7.grid(True)
                ax7.get_yaxis().get_major_formatter().set_useOffset(False)
                ax7.get_xaxis().get_major_formatter().set_useOffset(False)
                ax7.set_title("Positional Comparison", size=14)



                #DLS PLOT

                fig8, ax8 = plt.subplots(figsize=(6.5, 3.5))
                ax8.plot(survey_in["Station"], survey_in["DLS"], color = "orange", label = "Survey 1")
                ax8.plot(survey_out["Station"], survey_out["DLS"], color = "purple", label = "Survey 2")
                ax8.set_xlabel("Depth (m)", size = 14)
                ax8.set_ylabel("DLS/30m", size = 14)
                ax8.legend(loc = "best")
                ax8.grid(True)
                ax8.get_yaxis().get_major_formatter().set_useOffset(False)
                ax8.get_xaxis().get_major_formatter().set_useOffset(False)
                ax8.set_title("DLS Comparison", size=14)


                # UP and DOWN PLOT

                fig9, ax9 = plt.subplots(figsize=(6.5, 3.5))
                ax9.plot(survey_in["Station"], survey_in["UpDown"], color = "orange", label = "Survey 1")
                ax9.plot(survey_out["Station"], survey_out["UpDown"], color = "purple", label = "Survey 2")
                ax9.set_xlabel("Depth (m)", size = 14)
                ax9.set_ylabel("UP and Down (m)", size = 14)
                ax9.legend(loc = "best")
                ax9.grid(True)
                ax9.get_yaxis().get_major_formatter().set_useOffset(False)
                ax9.get_xaxis().get_major_formatter().set_useOffset(False)
                ax9.set_title("UP and Down Deviation", size=14)

                # LEFT and RIGHT PLOT

                fig10, ax10 = plt.subplots(figsize=(6.5, 3.5))
                ax10.plot(survey_in["Station"], survey_in["LeftRight"], color = "orange", label = "Survey 1")
                ax10.plot(survey_out["Station"], survey_out["LeftRight"], color = "purple", label = "Survey 2")
                ax10.set_xlabel("Depth (m)", size = 14)
                ax10.set_ylabel("Left and Right (m)", size = 14)
                ax10.legend(loc = "best")
                ax10.grid(True)
                ax10.get_yaxis().get_major_formatter().set_useOffset(False)
                ax10.get_xaxis().get_major_formatter().set_useOffset(False)
                ax10.set_title("Left and Right Deviation", size=14)

                # Target Deviation Plot - 2D (TOP)

                #Collar Coordinates
                collar_easting = survey_in["Easting"].iloc[0]
                collar_northing = survey_in["Northing"].iloc[0]
                collar_elevation = survey_in["Elevation"].iloc[0]

                #Collar Parameters
                collar_dip = float(self.lineEdit_6.text())
                collar_azimuth = float(self.lineEdit_7.text())

                # Calculating Target Coordinates
                target_easting = ((survey_out["Station"].iloc[-1] - survey_out["Station"].iloc[0]
                                   ) / 2 * ((np.sin(np.radians(collar_dip + 90)) * np.sin(np.radians(collar_azimuth))
                                            ) + (np.sin(np.radians(collar_dip + 90)) * np.sin(np.radians(collar_azimuth))))
                                  ) + collar_easting
                target_northing = ((survey_out["Station"].iloc[-1] - survey_out["Station"].iloc[0]
                                    ) / 2 * ((np.sin(np.radians(collar_dip + 90)) * np.cos(np.radians(collar_azimuth))
                                             ) + (np.sin(np.radians(collar_dip + 90)) * np.cos(np.radians(collar_azimuth))))
                                   ) + collar_northing

                target_elevation = (-1 * (survey_out["Station"].iloc[-1] - survey_out["Station"].iloc[0]
                                          ) / 2 * (np.cos(np.radians(collar_dip + 90)) + np.cos(np.radians(collar_dip + 90)))
                                    ) + collar_elevation



                #Actual Coordinates
                #Survey 01
                actual_easting1 = survey_in["Easting"].iloc[-1]
                actual_northing1 = survey_in["Northing"].iloc[-1]
                actual_elevation1 = survey_in["Elevation"].iloc[-1]
                #Survey 02
                actual_easting2 = survey_out["Easting"].iloc[-1]
                actual_northing2 = survey_out["Northing"].iloc[-1]
                actual_elevation2 = survey_out["Elevation"].iloc[-1]

                # Target Differences
                targ_east_differ1 = abs(target_easting - actual_easting1)
                targ_nort_differ1 = abs(target_northing - actual_northing1)
                targ_elev_differ1 = abs(target_elevation - actual_elevation1)

                targ_east_differ2 = abs(target_easting - actual_easting2)
                targ_nort_differ2 = abs(target_northing - actual_northing2)
                targ_elev_differ2 = abs(target_elevation - actual_elevation2)

                tot_misc_to_targ1 = np.sqrt(targ_east_differ1 ** 2 + targ_nort_differ1 ** 2 + targ_elev_differ1 ** 2)
                tot_misc_to_targ2 = np.sqrt(targ_east_differ2 ** 2 + targ_nort_differ2 ** 2 + targ_elev_differ2 ** 2)

                tot_misc_to_targ1_perc = tot_misc_to_targ1 / depth * 100
                tot_misc_to_targ2_perc = tot_misc_to_targ2 / depth * 100


                fig11, ax11 = plt.subplots(figsize=(6, 6))
                ax11.scatter(target_easting, target_northing,
                             marker = "o",
                             s = 300,
                             color = "green",
                             alpha = 0.5,
                             label = "Target")
                ax11.scatter(actual_easting1, actual_northing1,
                             marker = "o",
                             color = "orange",
                             label = "Survey 1")
                ax11.scatter(actual_easting2, actual_northing2,
                             marker = "o",
                             color = "purple",
                             label = "Survey 2")

                ax11.get_yaxis().get_major_formatter().set_useOffset(False)
                ax11.get_xaxis().get_major_formatter().set_useOffset(False)

                ax11.set_xlabel("Easting", size = 14, labelpad=0)
                ax11.set_ylabel("Northing", size = 14, labelpad=0)
                ax11.set_title("Distance From Target", size=15, pad = 28)
                #ax11.legend(loc = "best", markerscale  = 0.5)

                #Legend
                box = ax11.get_position()
                ax11.set_position([box.x0, box.y0 + box.height * 0.1,
                                   box.width, box.height * 0.9])

                # Put a legend below current axis
                ax11.legend(loc='upper center', bbox_to_anchor=(0.5, 1.09),
                            fancybox=True, shadow=False, ncol=5)

                #ax11.spines['left'].set_position(('data', target_easting))
                #ax11.spines['bottom'].set_position(('data', target_northing))

                ax11.tick_params(axis='both', which='major', pad=0)
                plt.xticks(rotation=40)
                plt.yticks(rotation=40)
                ax11.grid(True)

                ax11.xaxis.set_ticks_position('bottom')
                ax11.yaxis.set_ticks_position('left')
                ax11.spines['right'].set_color('none')
                ax11.spines['top'].set_color('none')

                #plt.xlim(target_easting-49, target_easting+45)
                #plt.ylim(target_northing-49, target_northing+49)

                # Target Deviation Plot - 3D

                #Planned Borehole data
                xdata_plan = np.linspace(collar_easting, target_easting, len(xdata_in))
                ydata_plan = np.linspace(collar_northing, target_northing, len(xdata_in))
                zdata_plan = np.linspace(collar_elevation, target_elevation, len(xdata_in))


                fig12 = plt.figure(figsize=(7.5, 7.5))
                ax12 = plt.axes(projection='3d')

                ax12.scatter3D(xdata_in, ydata_in, zdata_in, c="orange")
                ax12.plot(xdata_in, ydata_in, zdata_in, c="orange", label="Survey 1")
                ax12.scatter3D(xdata_out, ydata_out, zdata_out, c="purple")
                ax12.plot(xdata_out, ydata_out, zdata_out, c="purple", label ="Survey 2")
                ax12.scatter3D(xdata_plan, ydata_plan, zdata_plan, c="grey")
                ax12.plot(xdata_plan, ydata_plan, zdata_plan, c="grey", label ="Planned")
                plt.legend(loc="best")

                x_ticks = np.linspace(xdata_in.min(), xdata_in.max(), 5)
                y_ticks = np.linspace(ydata_in.min(), ydata_in.max(), 5)
                z_ticks = np.linspace(zdata_in.min(), zdata_in.max(), 5)

                ax12.set_xlabel('X', size = 14, labelpad=15)
                ax12.set_ylabel('Y', size = 14, labelpad=15)
                ax12.set_zlabel('Z', size = 14, labelpad=5)

                ax12.get_xaxis().get_major_formatter().set_useOffset(False)
                ax12.get_yaxis().get_major_formatter().set_useOffset(False)

                ## 3D Plot for first page

                fig13 = plt.figure(figsize=(6, 6))
                ax13 = plt.axes(projection='3d')

                # Data for three-dimensional scattered points
                xdata_in = survey_in["Easting"]
                ydata_in = survey_in["Northing"]
                zdata_in = survey_in["Elevation"]

                xdata_out = survey_out["Easting"]
                ydata_out = survey_out["Northing"]
                zdata_out = survey_out["Elevation"]

                ax13.scatter3D(xdata_in, ydata_in, zdata_in, c="orange")

                ax13.scatter3D(xdata_out, ydata_out, zdata_out, c="purple")


                ax13.axes.xaxis.set_ticklabels([])
                ax13.axes.yaxis.set_ticklabels([])
                ax13.axes.zaxis.set_ticklabels([])

                plt.box(on=None)


                #Generating PDF Report (Survey QC)





                script_dir = os.path.abspath(os.path.dirname(__file__)) # <-- absolute dir the script is in
                rel_path1 = "logo\\AT-GEOTECH-logo.png"
                rel_path2 = "logo\\dag_logo.jpg"
                rel_path3 = "logo\\BLASTO-logo-New.png"
                rel_path4 = "logo\\ATG_logo.jpg"
                logo_at_g = os.path     .join(script_dir, rel_path1)
                logo_azdg = os.path.join(script_dir, rel_path2)
                logo_blst = os.path.join(script_dir, rel_path3)
                logo_atg = os.path.join(script_dir, rel_path4)


                #logo_at_g = 'E:\MOOCs\My Projects\ReportINC\logo\AT-GEOTECH-logo.png'
                #logo_azdg = 'E:\MOOCs\My Projects\ReportINC\logo\dag_logo.jpg'
                #logo_blst = 'E:\MOOCs\My Projects\ReportINC\logo\BLASTO-logo-New.png'
                #logo_atg = 'E:\MOOCs\My Projects\ReportINC\logo\ATG_logo.jpg'
                logo_cb = logo_choose(self)
                if logo_cb == 0:
                        logo = logo_at_g
                        logo_w = 70
                        logo_h = 50
                if logo_cb == 1:
                        logo = logo_azdg
                        logo_w = 70
                        logo_h = 50
                if logo_cb == 2:
                        logo = logo_blst
                        logo_w = 70
                        logo_h = 50
                if logo_cb == 3:
                        logo = logo_atg
                        logo_w = 65
                        logo_h = 30

                #Set Canvas
                outfilename1 = project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) + \
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")" + "-QC Report.pdf"
                output_path = "Output"
                output_file1 = os.path.join(script_dir, output_path, outfilename1)
                #outfiledir1 = os.path.expanduser("~"),
                #outfilepath1 = os.path.join(os.path.expanduser("~"), "Documents/", outfilename1)
                pdf = canvas.Canvas(output_file1, pagesize=A4)
                pdf.setTitle("")
                pdf.setFont("Helvetica-Bold", 24)
                pdf.drawString(190, 790, "REFLEX - GYRO")


                # 1st Page
                imgdata = BytesIO()
                ax13 = plt.Axes(fig13, [0., 0., 1., 1.])
                ax13.set_axis_off()
                fig13.add_axes(ax13)
                fig13.savefig(imgdata, format='svg',dpi = 800)
                imgdata.seek(0)  # rewind the data
                Image1 = svg2rlg(imgdata)
                renderPDF.draw(Image1, pdf,21, 220)

                pdf.setFont("Helvetica", 18)
                pdf.drawString(233, 735, today)
                pdf.setFont("Helvetica-Bold", 20)
                pdf.drawString(155, 760, "QUALITY CHECK REPORT")

                pdf.setFont("Helvetica", 16)
                pdf.drawString(85, 230, "Project ID:  " + project_id)
                pdf.drawString(85, 210, "Borehole ID:  " + bh_id)
                pdf.drawString(85, 190, "Project location:  " + project_loc)
                pdf.drawString(85, 170, "Client:  " + client)
                pdf.drawString(85, 150, "Surveyor:  " + surveyed_by)
                pdf.drawString(85, 130, "Reporter:  " + report_by)
                pdf.drawString(85, 110, "Survey date:  " + survey_date)
                pdf.setFont("Helvetica", 14)
                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))


                pdf.drawImage(logo, 515, 775, width = logo_w, height = logo_h)
                pdf.showPage()

                # 2nd Page
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(160, 790, "DRILLING COLLAR PARAMETERS")

                pdf.setFont("Helvetica", 14)
                pdf.drawString(60, 765, "Easting:  " + str(round(collar_easting, 2)))
                pdf.drawString(60, 745, "Northing:  " + str(round(collar_northing, 2)))
                pdf.drawString(60, 725, "Elevation:  " + str(round(collar_elevation, 2)))
                pdf.setFont("Helvetica", 14)
                pdf.drawString(380, 765, "Dip:  " + str(collar_dip) + " deg")
                pdf.drawString(380, 745, "Azimuth:  " + str(collar_azimuth)+ " deg")
                pdf.drawString(380, 725, "Drill diameter:  " + str(drill_dia))
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(200, 700, "SURVEY PARAMETERS")
                pdf.setFont("Helvetica", 14)
                pdf.drawString(60, 640, "Survey interval:  " + str(station_inter) + " m")
                pdf.drawString(60, 620, "Number of stations:  " + str(num_stations))
                pdf.drawString(380, 680, "Survey run on:  " + str(survey_run))
                pdf.drawString(380, 660, "Angular units:  " + str(angular_unit))
                pdf.drawString(380, 640, "Linear units:  " + str(linear_unit))
                pdf.drawString(60, 680, "Survey start:  " + str(survey_start) + " m")
                pdf.drawString(60, 660, "Survey end:  " + str(survey_end) + " m")

                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(260, 600, "Survey 1")

                from reportlab.lib import colors
                from reportlab.lib.pagesizes import letter
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                width = 400
                height = 100

                #Survey 1
                x1 = 125
                y1 = 540

                t1=Table(s1_lol)
                t1.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                      ('TEXTCOLOR',(0,0),(0,0),colors.white)]))
                t1.wrapOn(pdf, width, height)
                t1.drawOn(pdf, x1, y1)

                #Survey 2
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(260, 520, "Survey 2")

                x2 = 125
                y2 = 460
                t2=Table(s2_lol)
                t2.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                      ('TEXTCOLOR',(0,0),(0,0),colors.white)]))
                t2.wrapOn(pdf, width, height)
                t2.drawOn(pdf, x2, y2)

                #Difference
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(70, 430, "End of Survey Difference")
                pdf.drawString(328, 430, "End of Survey Misclosure")
                x3 = 50
                y3 = 385
                t3=Table(end_of_surv_diff)
                t3.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                      ('TEXTCOLOR',(0,0),(0,0),colors.black)]))
                t3.wrapOn(pdf, width, height)
                t3.drawOn(pdf, x3, y3)

                #Misclosure table
                qc_pass = ('TEXTCOLOR',(-1,-1),(-1,-1), colors.green)
                qc_fail = ('TEXTCOLOR',(-1,-1),(-1,-1), colors.red)
                global color
                if misclosure <= depth * 1/100:
                    color = qc_pass
                else:
                    color = qc_fail

                x4 = 320
                y4 = 385
                t4=Table(end_of_surv_misc)
                t4.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
                                      color]))
                t4.wrapOn(pdf, width, height)
                t4.drawOn(pdf, x4, y4)

                #Misclosure plot
                imgdata1 = BytesIO()
                ax1 = plt.Axes(fig1, [0., 0., 1., 1.])
                ax1.set_axis_off()
                fig1.add_axes(ax1)
                fig1.savefig(imgdata1, format='svg',dpi = 800)
                imgdata1.seek(0)  # rewind the data
                Image2 = svg2rlg(imgdata1)
                renderPDF.draw(Image2, pdf,21, 100)

                pdf.setFont("Helvetica", 14)
                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))
                pdf.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf.showPage()

                # 3rd Page
                imgdata2 = BytesIO()
                ax2 = plt.Axes(fig2, [0., 0., 1., 1.])
                ax2.set_axis_off()
                fig2.add_axes(ax2)
                fig2.savefig(imgdata2, format='svg',dpi = 800)
                imgdata2.seek(0)  # rewind the data
                Image3 = svg2rlg(imgdata2)
                renderPDF.draw(Image3, pdf,-66, 70)
                pdf.setFont("Helvetica", 14)
                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))
                pdf.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf.showPage()

                # 4th Page
                imgdata3 = BytesIO()
                ax15 = plt.Axes(fig15, [0., 0., 1., 1.])
                ax15.set_axis_off()
                fig15.add_axes(ax15)
                fig15.savefig(imgdata3, format='svg',dpi = 800)
                imgdata3.seek(0)  # rewind the data
                Image4 = svg2rlg(imgdata3)
                renderPDF.draw(Image4, pdf,5, 450)

                imgdata4 = BytesIO()
                ax3 = plt.Axes(fig3, [0., 0., 1., 1.])
                ax3.set_axis_off()
                fig3.add_axes(ax3)
                fig3.savefig(imgdata4, format='svg',dpi = 800)
                imgdata4.seek(0)  # rewind the data
                Image5 = svg2rlg(imgdata4)
                renderPDF.draw(Image5, pdf,5, 90)
                pdf.setFont("Helvetica", 14)
                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))
                pdf.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf.showPage()

                # 5th Page
                #Easting
                imgdata5 = BytesIO()
                ax4 = plt.Axes(fig4, [0., 0., 1., 1.])
                ax4.set_axis_off()
                fig4.add_axes(ax4)
                fig4.savefig(imgdata5, format='svg',dpi = 800)
                imgdata5.seek(0)  # rewind the data
                Image6 = svg2rlg(imgdata5)
                renderPDF.draw(Image6, pdf,45, 580)

                #Northing
                imgdata6 = BytesIO()
                ax5 = plt.Axes(fig5, [0., 0., 1., 1.])
                ax5.set_axis_off()
                fig5.add_axes(ax5)
                fig5.savefig(imgdata6, format='svg',dpi = 800)
                imgdata6.seek(0)  # rewind the data
                Image7 = svg2rlg(imgdata6)
                renderPDF.draw(Image7, pdf,45, 320)

                #Elevation
                imgdata7 = BytesIO()
                ax6 = plt.Axes(fig6, [0., 0., 1., 1.])
                ax6.set_axis_off()
                fig6.add_axes(ax6)
                fig6.savefig(imgdata7, format='svg',dpi = 800)
                imgdata7.seek(0)  # rewind the data
                Image8 = svg2rlg(imgdata7)
                renderPDF.draw(Image8, pdf,45, 60)
                pdf.setFont("Helvetica", 14)
                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))
                pdf.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf.showPage()

                # 6th Page
                # Positional Comparison
                imgdata8 = BytesIO()
                ax7 = plt.Axes(fig7, [0., 0., 1., 1.])
                ax7.set_axis_off()
                fig7.add_axes(ax7)
                fig7.savefig(imgdata8, format='svg',dpi = 800)
                imgdata8.seek(0)  # rewind the data
                Image9 = svg2rlg(imgdata8)
                renderPDF.draw(Image9, pdf,30, 490)

                # DLS
                imgdata9 = BytesIO()
                ax8 = plt.Axes(fig8, [0., 0., 1., 1.])
                ax8.set_axis_off()
                fig8.add_axes(ax8)
                fig8.savefig(imgdata9, format='svg',dpi = 800)
                imgdata9.seek(0)  # rewind the data
                Image10 = svg2rlg(imgdata9)
                renderPDF.draw(Image10, pdf,30, 90)

                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))
                pdf.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf.showPage()

                # 7th Page
                # Ip and Down
                imgdata10 = BytesIO()
                ax9 = plt.Axes(fig9, [0., 0., 1., 1.])
                ax9.set_axis_off()
                fig9.add_axes(ax9)
                fig9.savefig(imgdata10, format='svg', dpi=800)
                imgdata10.seek(0)  # rewind the data
                Image11 = svg2rlg(imgdata10)
                renderPDF.draw(Image11, pdf, 30, 490)

                # Left and Right
                imgdata11 = BytesIO()
                ax10 = plt.Axes(fig10, [0., 0., 1., 1.])
                ax10.set_axis_off()
                fig10.add_axes(ax10)
                fig10.savefig(imgdata11, format='svg', dpi=800)
                imgdata11.seek(0)  # rewind the data
                Image12 = svg2rlg(imgdata11)
                renderPDF.draw(Image12, pdf, 30, 90)


                page_number = pdf.getPageNumber()
                pdf.drawString(500, 20, "Page " + str(page_number))
                pdf.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf.save()

                #Generating PDF Report (Drilling QC)

                planned_actual_t = [[bh_id, "Planned", "Actual"], ["Dip", collar_dip, round(survey_out["Dip"].iloc[-1])],
                                    ["Azimuth", collar_azimuth, round(survey_out["Azimuth"].iloc[-1])]]

                misc_to_target_t = [["Survey Name", "Survey 1", "Survey 2"],
                                    ["Easting Difference (m)", round(targ_east_differ1, 2), round(targ_east_differ2, 2)],
                                   ["Northing Difference (m)", round(targ_nort_differ1, 2), round(targ_nort_differ2, 2)],
                                   ["Elevation Difference (m)",round(targ_elev_differ1, 2), round(targ_elev_differ2, 2)],
                                   ["Total Misclosure (m)", round(tot_misc_to_targ1, 2), round(tot_misc_to_targ2, 2)],
                                   ["Percentage Misclosure %", round(tot_misc_to_targ1_perc, 2), round(tot_misc_to_targ2_perc, 2)]]



                #PDF 2
                outfilename2 = project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) + \
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")" + "-Drilling Report.pdf"
                output_path = "Output"
                output_file2 = os.path.join(script_dir, output_path, outfilename2)
                #outfiledir2 = os.path.expanduser("~"),
                #outfilepath2 = os.path.join(os.path.expanduser("~"), "Documents/", outfilename2)

                pdf2 = canvas.Canvas(output_file2, pagesize=A4)
                pdf2.setTitle("")

                # 1st Page
                # Target plot
                imgdata1 = BytesIO()
                # ax11 = plt.Axes(fig11, [0., 0., 1., 1.])
                # ax11.set_axis_off()
                # fig11.add_axes(ax11)
                fig11.savefig(imgdata1, format='svg', dpi=fig11.dpi)
                # fig11.savefig(imgdata1, format='svg',dpi = 800)
                imgdata1.seek(0)  # rewind the data
                Image1 = svg2rlg(imgdata1)
                # Image1._showBoundary = False
                renderPDF.draw(Image1, pdf2, 40, 185)

                pdf2.setFont("Helvetica-Bold", 24)
                pdf2.drawString(90, 745, "DRILLING QUALITY CHECK REPORT")


                # target tabele
                x1 = 380
                y1 = 113

                t1 = Table(planned_actual_t)
                t1.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('TEXTCOLOR', (0, 0), (0, 0), colors.black)]))
                t1.wrapOn(pdf2, width, height)
                t1.drawOn(pdf2, x1, y1)

                # Misclosure to target tabele
                pdf2.setFont("Helvetica-Bold", 16)
                pdf2.drawString(220, 180, "Misclosure to Target")

                x2 = 80
                y2 = 60

                t2 = Table(misc_to_target_t)
                t2.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('TEXTCOLOR', (0, 0), (0, 0), colors.black)]))
                t2.wrapOn(pdf2, width, height)
                t2.drawOn(pdf2, x2, y2)
                pdf2.setFont("Helvetica", 14)
                page_number = pdf2.getPageNumber()
                pdf2.drawString(500, 20, "Page " + str(page_number))
                pdf2.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                               ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf2.drawImage(logo, 515, 775, width=logo_w, height=logo_h)
                pdf2.showPage()

                # 3D PLOT of DEVIATION FROM TARGET

                imgdata2 = BytesIO()
                ax12 = plt.Axes(fig12, [0., 0., 1., 1.])
                ax12.set_axis_off()
                fig12.add_axes(ax12)
                fig12.savefig(imgdata2, format='svg',dpi = 800)
                imgdata2.seek(0)  # rewind the data
                Image2 = svg2rlg(imgdata2)
                renderPDF.draw(Image2, pdf2, -50, 100)

                pdf2.setFont("Helvetica", 20)
                pdf2.drawString(140, 720, "Planned and Actual Borehole Paths")
                pdf2.setFont("Helvetica", 14)
                page_number = pdf2.getPageNumber()
                pdf2.drawString(500, 20, "Page " + str(page_number))
                pdf2.drawString(45, 20, project_id + "-" + bh_id + " " + "(" + str(survey_in["Station"].iloc[0]) +
                                ".0m" + "-" + str(survey_in["Station"].iloc[-1]) + ".0m" + ")")
                pdf2.save()
                return generate_report
except Exception:
    traceback.print_exc()
    while(True):
        pass