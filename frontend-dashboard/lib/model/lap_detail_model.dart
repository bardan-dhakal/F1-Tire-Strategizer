import 'dart:ui';

enum TyreCompound { soft, medium, hard, intermediate, wet }

extension TyreCompoundExtension on TyreCompound {
  String get displayName {
    switch (this) {
      case TyreCompound.soft:
        return 'SOFT';
      case TyreCompound.medium:
        return 'MEDIUM';
      case TyreCompound.hard:
        return 'HARD';
      case TyreCompound.intermediate:
        return 'INTERMEDIATE';
      case TyreCompound.wet:
        return 'WET';
    }
  }

  Color get color {
    switch (this) {
      case TyreCompound.soft:
        return const Color(0xFFE10600);
      case TyreCompound.medium:
        return const Color(0xFFF1EB00);
      case TyreCompound.hard:
        return const Color(0xFFFFFFFF);
      case TyreCompound.intermediate:
        return const Color(0xFF00D2BE);
      case TyreCompound.wet:
        return const Color(0xFF006F62);
    }
  }
}

enum WearPattern { uneven, inner, outer, center, even }

extension WearPatternExtension on WearPattern {
  String get displayName {
    switch (this) {
      case WearPattern.uneven:
        return 'Uneven';
      case WearPattern.inner:
        return 'Inner';
      case WearPattern.outer:
        return 'Outer';
      case WearPattern.center:
        return 'Center';
      case WearPattern.even:
        return 'Even';
    }
  }
}

enum TyreColor { matteBlack, glossyBlack, purpleTin, greyBlack, paleGrey }

extension TyreColorExtension on TyreColor {
  String get displayName {
    switch (this) {
      case TyreColor.matteBlack:
        return 'Matte';
      case TyreColor.glossyBlack:
        return 'Glossy';
      case TyreColor.purpleTin:
        return 'Purple';
      case TyreColor.greyBlack:
        return 'Grey';
      case TyreColor.paleGrey:
        return 'Pale';
    }
  }
}

class TyreModel {
  final int lapNumber;
  final TyreCompound compound;
  final int trackTemperature;
  final String strategy;
  final String track;
  final String trackKnowledge;
  final TyreDetailModel frontLeft;
  final TyreDetailModel frontRight;
  final TyreDetailModel rearLeft;
  final TyreDetailModel rearRight;

  TyreModel({
    required this.strategy,
    required this.track,
    required this.trackKnowledge,
    required this.lapNumber,
    required this.compound,
    required this.trackTemperature,
    required this.frontLeft,
    required this.frontRight,
    required this.rearLeft,
    required this.rearRight,
  });
}

class TyreDetailModel {
  final TyreColor color;
  final WearPattern wearPattern;
  final bool sidewallDefomation;
  final bool isGraining;
  final int tyrePressure;
  final int tyreTemperature;

  TyreDetailModel({
    required this.color,
    required this.wearPattern,
    required this.sidewallDefomation,
    required this.isGraining,
    required this.tyrePressure,
    required this.tyreTemperature,
  });
}
