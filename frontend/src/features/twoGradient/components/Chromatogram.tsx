import React from "react";
import { useD3 } from "../hooks/useD3";
import * as d3 from "d3";
// import "../../../css/style.css";
import { usePredict } from "../api/predict";

const C = 100;

const getPeakHeight = (peak: any) => {
  return peak.area / (Math.sqrt(Math.PI) * C);
};

const getYValue = (peak: any, x: number) => {
  const height = getPeakHeight(peak);
  return (
    height *
    Math.exp(-(Math.pow(x - peak.position, 2) / Math.pow(peak.width / 2, 2)))
  );
};

const assemblePeakData = (result: any) => {
  const peakData = [];
  for (let i = 0; i < result.retention_times.length; i++) {
    peakData.push({
      position: result.retention_times[i],
      width: result.widths[i],
      area: result.areas[i],
    });
  }
  return peakData;
};

const getPeakRanges = (peakData: any) => {
  const peakRanges: any = [];
  peakData.forEach((peak: any) => {
    peakRanges.push({
      start: peak.position - peak.width / 2 - 0.5,
      end: peak.position + peak.width / 2 + 0.5,
    });
  });
  return peakRanges;
};

const generateHeterogenousRange = (peakRanges: any, tg: number) => {
  let stepConst = 0.01;

  let resultArray = [0];

  peakRanges.forEach((peakRange: any) => {
    for (let i = peakRange.start; i < peakRange.end; i += stepConst) {
      if (resultArray.slice(-1)[0] < i) {
        resultArray.push(i);
      }
    }
  });

  resultArray.push(tg);

  return resultArray;
};

type ChromatogramProps = {
  bValue: number[];
};

export function Chromatogram({ bValue }: ChromatogramProps) {
  const results = usePredict().data?.results;
  let currentPeakData: any = [];

  const currentPeak =
    results !== undefined
      ? results.filter(
          (item: any) =>
            Math.round(item.conditions.initial * 100) / 100 === bValue[0] &&
            Math.round(item.conditions.final * 100) / 100 === bValue[1]
        )
      : [];
  if (currentPeak.length > 0) {
    currentPeakData = assemblePeakData(currentPeak[0]);
  }

  const peakRanges = getPeakRanges(currentPeakData);
  const heterogenousRange = generateHeterogenousRange(peakRanges, 15);

  const ref = useD3(
    (svg: any) => {
      svg.selectAll("*").remove();

      const xValues = heterogenousRange;
      const yValues = xValues.map((x) => {
        const sum = d3.sum(currentPeakData, (peak: any) => getYValue(peak, x));
        return sum;
      });

      var parent = svg.node().parentElement;
      var svgWidth = parent.clientWidth;
      var svgHeight = parent.clientHeight;

      const root = svg.append("g");
      root.attr("transform", undefined);

      const margin = { top: 50, right: 70, bottom: 50, left: 70 };

      const xAxisGroup = root
        .append("g")
        .attr(
          "transform",
          `translate(${margin.left}, ${svgHeight - margin.bottom})`
        );

      const yAxisGroup = root
        .append("g")
        .attr(
          "transform",
          `translate(${margin.left}, ${svgHeight - margin.bottom})`
        );

      const xScale = d3
        .scaleLinear()
        .domain(d3.extent(xValues) as number[])
        .range([0, svgWidth - margin.left - margin.right]);

      const yScale = d3
        .scaleLinear()
        .domain([0, d3.max(yValues) as number])
        .range([0, -(svgHeight - margin.top - margin.bottom)]);

      const xAxis = d3.axisBottom(xScale);
      const yAxis = d3.axisLeft(yScale);

      xAxisGroup.call(xAxis);
      yAxisGroup.call(yAxis);

      const line = d3
        .line()
        .x((d: any) => xScale(d[0]))
        .y((d: any) => yScale(d[1]));

      root
        .append("path")
        .datum(d3.zip(xValues, yValues))
        .attr("d", line)
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr(
          "transform",
          `translate(${margin.left}, ${svgHeight - margin.bottom})`
        );
    },
    [bValue, results]
  );

  return <svg ref={ref} height="100%" width="100%" />;
}
